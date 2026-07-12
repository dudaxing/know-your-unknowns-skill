import hashlib
import zipfile
from pathlib import Path

root = Path(r"D:/Coding/know-your-unkowns")
skill = root / "know-your-unknowns"
zpath = root / "dist" / "know-your-unknowns.skill"
files = [p for p in skill.rglob("*") if p.is_file()]
with zipfile.ZipFile(zpath) as z:
    names = z.namelist()
    assert len(names) == len(set(names)), "dup entries"
    exp = {"know-your-unknowns/" + p.relative_to(skill).as_posix() for p in files}
    assert set(names) == exp, (exp - set(names), set(names) - exp)
    for p in files:
        n = "know-your-unknowns/" + p.relative_to(skill).as_posix()
        data = z.read(n)
        assert (zipfile.crc32(data) & 0xFFFFFFFF) == z.getinfo(n).CRC
        assert hashlib.sha256(data).digest() == hashlib.sha256(p.read_bytes()).digest()
print("pack ok", len(files), "files")
