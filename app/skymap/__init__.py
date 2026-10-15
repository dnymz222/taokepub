from flask import Blueprint
from pathlib import Path

# 引擎仓库根（与 astronomyobserver/ 同级），页面里写死了 ../../build/ 和
# ../test-skydata/ 的相对引用，所以整体挂在一个 URL 前缀下、层级不能变。
ENGINE_ROOT = Path(__file__).resolve().parent.parent / "stellarium-web-engine-master"


print(ENGINE_ROOT)

skymap = Blueprint(
    "skymap",
    __name__,
    static_folder=str(ENGINE_ROOT),
    static_url_path="/skymap",
)



