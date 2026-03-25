import os
import sys
from PIL import Image, ImageOps

def process_and_copy_images(input_dir, output_dir):
    if not os.path.exists(input_dir):
        print(f"錯誤：找不到輸入目錄 {input_dir}")
        return

    # os.walk 會走訪 input_dir 下所有的資料夾與檔案
    for root, dirs, files in os.walk(input_dir):
        # 計算出當前所在目錄相對於 input_dir 的相對路徑
        # 例如 root 是 "./data_raw/羊蹄甲/20260322"，相對路徑就是 "羊蹄甲/20260322"
        rel_path = os.path.relpath(root, input_dir)

        # 組合出對應的輸出目錄路徑
        target_dir = os.path.join(output_dir, rel_path)

        # 如果該輸出目錄不存在，則建立它（維持樹狀結構）
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                in_path = os.path.join(root, filename)
                out_path = os.path.join(target_dir, filename)

                try:
                    # 讀取圖片，轉為 RGB 以防 PNG 的透明通道報錯
                    img = Image.open(in_path).convert("RGB")

                    # 進行等比壓縮與 padding
                    img_padded = ImageOps.pad(img, (224, 224), color=(0, 0, 0))

                    # 儲存到新的資料夾中，格式統一是 JPEG，壓縮品質 85
                    img_padded.save(out_path, "JPEG", quality=85)
                    print(f"已處理並儲存: {out_path}")
                except Exception as e:
                    print(f"❌ 處理 {in_path} 時發生錯誤: {e}")

    print("\n✅ 所有圖片處理與壓縮完成！")

if __name__ == "__main__":
    # 檢查命令列參數
    if len(sys.argv) != 3:
        print("用法: python process_data_raw.py <輸入目錄> <輸出目錄>")
        print("範例: python process_data_raw.py ./data_raw ./data")
        sys.exit(1)

    in_dir = sys.argv[1]
    out_dir = sys.argv[2]

    process_and_copy_images(in_dir, out_dir)
