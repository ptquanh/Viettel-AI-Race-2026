import os
import csv
import struct
import argparse
from pathlib import Path
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ==========================================
# COLMAP PARSING UTILS
# ==========================================
PRIVATE_SET_NAME='private_set1'

CAMERA_MODELS = {
    0: ('SIMPLE_PINHOLE', 3), 1: ('PINHOLE', 4), 2: ('SIMPLE_RADIAL', 4),
    3: ('RADIAL', 5), 4: ('OPENCV', 8), 5: ('OPENCV_FISHEYE', 8),
    6: ('FULL_OPENCV', 12), 7: ('FOV', 5), 8: ('SIMPLE_RADIAL_FISHEYE', 4),
    9: ('RADIAL_FISHEYE', 5), 10: ('THIN_PRISM_FISHEYE', 12),
}

def read_cameras_binary(path_to_model_file):
    """
    Đọc file cameras.bin của COLMAP.
    Trả về dict: {camera_id: {'model': name, 'width': w, 'height': h, 'params': [p1, ...]}}
    """
    cameras = {}
    with open(path_to_model_file, "rb") as f:
        num_cameras = struct.unpack('<Q', f.read(8))[0]
        for _ in range(num_cameras):
            camera_id, model_id, width, height = struct.unpack('<iiQQ', f.read(24))
            model_name, num_params = CAMERA_MODELS[model_id]
            params = struct.unpack('<' + 'd' * num_params, f.read(8 * num_params))
            cameras[camera_id] = {
                "id": camera_id,
                "model": model_name,
                "width": width,
                "height": height,
                "params": params
            }
    return cameras

def read_images_binary(path_to_model_file):
    """
    Đọc file images.bin của COLMAP.
    Trả về dict: {image_id: {'name': name, 'camera_id': id, 'q': [qw,qx,qy,qz], 't': [tx,ty,tz], 'num_points2D': n}}
    """
    images = {}
    with open(path_to_model_file, "rb") as f:
        num_images = struct.unpack('<Q', f.read(8))[0]
        for _ in range(num_images):
            # 1 int (id) + 4 doubles (q) + 3 doubles (t) + 1 int (camera_id) = 64 bytes
            image_id, qw, qx, qy, qz, tx, ty, tz, camera_id = struct.unpack('<idddddddi', f.read(64))
            
            # Read name string
            name_bytes = bytearray()
            while True:
                ch = f.read(1)
                if ch == b'': raise EOFError('Unexpected EOF')
                if ch == b'\x00': break
                name_bytes += ch
            name = name_bytes.decode('utf-8')
            
            # Read 2D points (x, y, point3D_id)
            num_points2D = struct.unpack('<Q', f.read(8))[0]
            # Bỏ qua việc lưu chi tiết point2D để tiết kiệm RAM, chỉ lưu số lượng
            f.seek(24 * num_points2D, 1) # 2 doubles + 1 uint64 = 24 bytes/point
            
            images[image_id] = {
                "id": image_id,
                "name": name,
                "camera_id": camera_id,
                "q": (qw, qx, qy, qz),
                "t": (tx, ty, tz),
                "num_points2D": num_points2D
            }
    return images

def read_points3D_binary(path_to_model_file):
    """
    Đọc file points3D.bin của COLMAP.
    Trả về số lượng điểm 3D thưa.
    """
    with open(path_to_model_file, "rb") as f:
        num_points = struct.unpack('<Q', f.read(8))[0]
    return num_points

# ==========================================
# TEST POSES CSV PARSING
# ==========================================
def read_test_poses(csv_path):
    """
    Đọc file test_poses.csv.
    Trả về list các dict chứa thông số camera cần sinh.
    """
    poses = []
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            poses.append({
                "image_name": row["image_name"],
                "q": (float(row["qw"]), float(row["qx"]), float(row["qy"]), float(row["qz"])),
                "t": (float(row["tx"]), float(row["ty"]), float(row["tz"])),
                "focal": (float(row["fx"]), float(row["fy"])),
                "principal": (float(row["cx"]), float(row["cy"])),
                "resolution": (int(row["width"]), int(row["height"]))
            })
    return poses

# ==========================================
# MAIN EXTRACTION FUNCTION
# ==========================================
def extract_scene_features(scene_dir):
    """
    Bóc tách đặc trưng của 1 scene cụ thể.
    Trả về dict chứa các thông số.
    """
    scene_dir = Path(scene_dir)
    train_dir = scene_dir / "train"
    test_dir = scene_dir / "test"
    
    features = {
        "Scene": scene_dir.name,
        "Train Images": 0,
        "Camera Model": "N/A",
        "Resolution": "N/A",
        "Extrinsics": 0,
        "3D Points": 0,
        "Test Poses": 0
    }
    
    # 1. Đếm số lượng ảnh gốc
    train_images_dir = train_dir / "images"
    if train_images_dir.exists():
        features["Train Images"] = len([f for f in train_images_dir.iterdir() if f.is_file()])

    # 2. Bóc tách dữ liệu COLMAP (Sparse Reconstruction)
    sparse_dir = train_dir / "sparse" / "0"
    if sparse_dir.exists():
        cameras_file = sparse_dir / "cameras.bin"
        images_file = sparse_dir / "images.bin"
        points3D_file = sparse_dir / "points3D.bin"
        
        if cameras_file.exists():
            cameras = read_cameras_binary(cameras_file)
            if cameras:
                cam = list(cameras.values())[0]
                features["Camera Model"] = cam['model']
                features["Resolution"] = f"{cam['width']}x{cam['height']}"
                
        if images_file.exists():
            images = read_images_binary(images_file)
            features["Extrinsics"] = len(images)
            
        if points3D_file.exists():
            features["3D Points"] = read_points3D_binary(points3D_file)

    # 3. Bóc tách Test Poses
    test_csv_file = test_dir / "test_poses.csv"
    if test_csv_file.exists():
        test_poses = read_test_poses(test_csv_file)
        features["Test Poses"] = len(test_poses)

    return features

def main(data_dir):
    data_dir = Path(data_dir)
    scenes = []
    
    print(f"Đang quét thư mục: {data_dir.absolute()}")
    
    for split in ['public_set', PRIVATE_SET_NAME]:
        split_dir = data_dir / split
        if not split_dir.exists():
            continue
            
        for scene_dir in split_dir.iterdir():
            if scene_dir.is_dir() and (scene_dir / "train").exists():
                feat = extract_scene_features(scene_dir)
                feat["Split"] = split
                scenes.append(feat)
                print(f" - Bóc tách thành công: {split}/{scene_dir.name}")
                
    if not scenes:
        print(f"Không tìm thấy scene nào trong {data_dir}!")
        return
        
    md_path = Path("features_summary.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Tổng hợp Đặc trưng Dữ liệu (Viettel AI Race)\n\n")
        f.write("| Split | Scene | Train Images | Camera Model | Resolution | COLMAP Poses | 3D Points | Test Poses |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        
        # Sort by Split, then Scene name
        scenes_sorted = sorted(scenes, key=lambda x: (x["Split"], x["Scene"]))
        for s in scenes_sorted:
            f.write(f"| {s['Split']} | {s['Scene']} | {s['Train Images']} | {s['Camera Model']} | {s['Resolution']} | {s['Extrinsics']} | {s['3D Points']} | {s['Test Poses']} |\n")
            
    print(f"\n✅ Đã bóc tách xong! Vui lòng mở file '{md_path.absolute()}' để xem kết quả dạng bảng.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bóc tách đặc trưng toàn bộ input Viettel AI Race")
    parser.add_argument("--data_dir", type=str, default="../input/phase1", help="Đường dẫn đến thư mục phase1 chứa public_set và private_set")
    args = parser.parse_args()
    
    main(args.data_dir)
