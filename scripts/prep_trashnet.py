import os, shutil, random

SRC = "datasets/trashnet"
DST = "data"
split = 0.8
random.seed(42)


img_ext = {"jpg", "jpeg", "png", "webp", "bmp"}

table_content = {"cardboard": "recycle",
                 "glass": "recycle",
                 "metal": "recycle",
                 "paper": "recycle",
                 "plastic": "recycle",
                 "trash": "landfill"}

def is_image(filename): 
    if "." not in filename:
        return False
    else: 
        ext = filename.rsplit(".", 1)[-1].lower()
        return ext in img_ext
    
def safe_move(src_path: str, dst_dir: str):
    os.makedirs(dst_dir, exist_ok=True)
    base = os.path.splitext(os.path.basename(src_path))[0]
    ext  = os.path.splitext(os.path.basename(src_path))[1]
    new_path = os.path.join(dst_dir, base + ext)
    i = 1
    while os.path.exists(new_path):
        new_path = os.path.join(dst_dir, f"{base}_{i}{ext}")
        i += 1
    shutil.copy2(src_path, new_path)


    
for k, v in table_content.items():
    src_dir = os.path.join(SRC, k)
    files = []
    if not os.path.isdir(src_dir):
        print("[SKIP]", src_dir)
        continue

    for n in os.listdir(src_dir):
        if is_image(n):
            files.append(n)
    
    random.shuffle(files)
    split_idx = int(len(files) * split)
    train_files = (files[:split_idx])
    val_files = (files[split_idx:])

    dst_train_dir = os.path.join(DST, "train", v)
    dst_val_dir = os.path.join(DST, "val", v)

    for filename in train_files:
        src = os.path.join(src_dir, filename)
        safe_move(src, dst_train_dir)
    
    for filename in val_files:
        src = os.path.join(src_dir, filename)
        safe_move(src, dst_val_dir)

    print(f"[OK] {k:10s} → {v:9s} | train {len(train_files):4d} | val {len(val_files):4d}")

    
    



    
