import random
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import qrcode


def generate_certificate(name, level, cert_id, qr_data, output_path='certificate_images/certificate2.png'):
    # 加载证书背景图片
    background = Image.open("certificate_images/new_certificate_template.png").convert("RGB")

    # 准备绘图
    draw = ImageDraw.Draw(background)

    # 加载字体（可替换为你自己的路径和字体）
    font_name = ImageFont.truetype(
        "fonts/SourceSans3-SemiBold.ttf", size=160)
    font_level = ImageFont.truetype(
        "fonts/SourceSans3-Bold.ttf", size=90)
    font_info = ImageFont.truetype(
        "fonts/SourceSans3-regular.ttf", size=78)

    # 写入文字内容
    # Name
    draw.text((background.width/2, background.height/3+150),
              name, fill="#033753", font=font_name, anchor='mm')
    # Level
    draw.text((background.width/3 - 245, background.height/2 - 112),
              level, fill="black", font=font_level)
    # certification ID
    draw.text(
        (background.width/2 - 12, background.height/2+88), cert_id, fill="black", font=font_info)
    # graph name
    draw.text(
        (background.width/2 - 12, background.height/2+184), "Xlore", fill="black", font=font_info)
    # system
    draw.text(
        (background.width/2 - 12, background.height/2+278), "EduKG Certification Platform", fill="black", font=font_info)
    # date issued
    draw.text(
        (background.width/2 - 12, background.height/2+374), datetime.now().strftime('%B %d, %Y'), fill="black", font=font_info)
    # valid until
    future_year = datetime.now().year + 2  # year calculation
    draw.text(
        (background.width/2 - 12, background.height/2+472), datetime.now().strftime(f'%B %d, {future_year}'), fill="black", font=font_info)

    # 生成二维码（二维码内容可替换为你想要的链接或ID）
    qr = qrcode.make(qr_data)

    # 缩放二维码到适当大小（如 300x300）
    qr = qr.resize((200, 200))

    # 粘贴二维码到背景图上（右下角或其他你想要的位置）
    background.paste(qr, (background.width - 250, background.height - 250))

    # 保存为 PDF
    background.save(output_path, "PNG")


# 示例调用
# from generate_id import generate_unique_random
# id = generate_unique_random()
# id = f'EDUKG-{datetime.now().strftime('%Y%m%d')}-{num:03d}'
# generate_certificate("Beijing Zhipu Huazhang Technology Co., Ltd.", "Level II Conformance", id, "DJczaQP8zXpYwC3mbGXIht8ktZ7o6GfzV1T95w7GkjdTm7fBJzvCxJAPh/bxlrbT3GYeUC+Bv4jW5E4d53KDhn0TEVue5AvvNiq4lGUlVuW2vNQ/iOu7D+cnS3fsnUb/GjUMyO3Eww36XgWRQ1NZrf8Ts+kHrcLocuS4fHCyLDEzZb86265CWTcqudT66/x7QDSsjZldkDOCF8rJ3QuUF/ng25atdADmCzotc+z8vUzWvXrl9PIy6/OxDKfKZuf/VI2NIpclLDrws0K4OcLMnv2SQpYGPrts3cTRcNmgqtcc8HcfFu1KAz4tnoKu97ptGkilUpEv/5YLafTX+SQLuA==")
