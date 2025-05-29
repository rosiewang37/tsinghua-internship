from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import qrcode

def generate_certificate(name, cert_id, output_path='certificate.pdf'):
    # 加载证书背景图片
    background = Image.open("certificate.png").convert("RGB")

    # 准备绘图
    draw = ImageDraw.Draw(background)

    # 加载字体（可替换为你自己的路径和字体）
    font_name = ImageFont.truetype("SourceSans3-VariableFont_wght.ttf", size=200)
    font_info = ImageFont.truetype("SourceSans3-VariableFont_wght.ttf", size=100)

    # 写入文字内容
    draw.text((500, 1270), name, fill="black", font=font_name)
    draw.text((500, 1670), f"Certification ID: {cert_id}", fill="black", font=font_info)
    draw.text((500, 2000), f"Certification Time: {datetime.now().strftime('%Y-%m-%d')}", fill="black", font=font_info)

    # 生成二维码（二维码内容可替换为你想要的链接或ID）
    qr_data = "DJczaQP8zXpYwC3mbGXIht8ktZ7o6GfzV1T95w7GkjdTm7fBJzvCxJAPh/bxlrbT3GYeUC+Bv4jW5E4d53KDhn0TEVue5AvvNiq4lGUlVuW2vNQ/iOu7D+cnS3fsnUb/GjUMyO3Eww36XgWRQ1NZrf8Ts+kHrcLocuS4fHCyLDEzZb86265CWTcqudT66/x7QDSsjZldkDOCF8rJ3QuUF/ng25atdADmCzotc+z8vUzWvXrl9PIy6/OxDKfKZuf/VI2NIpclLDrws0K4OcLMnv2SQpYGPrts3cTRcNmgqtcc8HcfFu1KAz4tnoKu97ptGkilUpEv/5YLafTX+SQLuA=="
    qr = qrcode.make(qr_data)

    # 缩放二维码到适当大小（如 300x300）
    qr = qr.resize((200, 200))

    # 粘贴二维码到背景图上（右下角或其他你想要的位置）
    background.paste(qr, (background.width - 250, background.height - 250))

    # 保存为 PDF
    background.save(output_path, "PDF")

# 示例调用
generate_certificate("San Zhang", "IEEE-TTL-20250513-001")
