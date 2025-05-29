from rdflib import Graph
from pyld import jsonld
import json
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime
import base64
from generate_id import generate_unique_random
from new_certificate import generate_certificate

def certify(ttl_document, user_name, level_of_conformance):
    # 1. 加载 TTL 文件
    g = Graph()
    g.parse(ttl_document, format="ttl")

    # 2. 转换为 JSON-LD
    jsonld_data = json.loads(g.serialize(format="json-ld"))

    # 3. 使用 URDNA2015 规范化为 N-Quads
    # Converts the JSON-LD data to a consistent form (so that two logically identical graphs will always produce the exact same output) using the URDNA2015 normalization algorithm
    normalized = jsonld.normalize(
    jsonld_data,
    {"algorithm": "URDNA2015", "format": "application/n-quads"}
    )

    # 4. 对 normalized 数据进行 SHA-256 哈希
    # convert raw binary data into a fixed-size string of bytes (32-byte (256-bit))
    # utf-8 convert strings to bytes
    # .digest() returns the binary hash of the input
    hash_digest = hashlib.sha256(normalized.encode("utf-8")).digest()

    # 5. 加载私钥（例如从 PEM 文件加载）
    # rb: read binary mode
    # with open(...) as key_file: automatically closes file afterwards
    # serialization: read and parse the contents of the PEM file (a standard format for storing cryptographic keys)
    # turns the raw file data into a usable RSA private key object 
    # RSA private key object: digitally sign, decrypt data
    with open("private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    # 6. 使用 RSA 对哈希进行签名
    signature = private_key.sign(
    hash_digest,
    padding.PKCS1v15(),  # 或者使用 PSS 作为 padding
    hashes.SHA256()
    )


    # 5. 加载私钥（例如从 PEM 文件加载）
    public_key = private_key.public_key()

    # 获取公钥 PEM
    pub_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    # 生成签名证书结构
    certificate = {
    "signature": base64.b64encode(signature).decode('utf-8'),
    "signed_at": datetime.utcnow().isoformat() + "Z",
    "public_key": {
        "key_type": "RSA",
        "key_size": 2048,
        "pem": pub_pem
    },
    "issuer": {
        "name": "edukg certification office",
        "id": "https://edukg.org",
        "contact": "edukg.org@gmail.com"
    }
    }

    # 写入文件
    with open("certificate.json", "w") as f:
        json.dump(certificate, f, indent=2)

    # generate ID
    id = generate_unique_random()

    # generate hash string
    hash_hex = hash_digest.hex()

    # generate certificate and save it to '.png'
    generate_certificate(user_name, level_of_conformance, id, hash_hex, 'certificate_images/certificate_rosie.png')

# example using the certify function
certify("biology.ttl", "Rosie Wang", "Level II Conformance")