#coding=utf8
from app import db
class JiliangCert(db.Model):
    __tablename__ = "JiliangCerts"

    cert_id = db.Column(db.String, primary_key=True)   # 证书编号
    company = db.Column(db.String)                    # 送检单位
    instrument_name = db.Column(db.String)            # 计量器具名称
    model = db.Column(db.String)                      # 型号规格
    serial_number = db.Column(db.String)              # 出厂编号
    manage_id = db.Column(db.String)                  # 管理编号
    approver = db.Column(db.String)                   # 批准人
    inspector = db.Column(db.String)                  # 核验员
    verifier = db.Column(db.String)                   # 检定员
    check_date = db.Column(db.String)                 # 检校日期

    def to_dict(self):
        """返回给前端的中文字段字典"""
        return {
            "证书编号": self.cert_id,
            "送检单位": self.company,
            "计量器具名称": self.instrument_name,
            "型号规格": self.filterdian(self.model),
            "出厂编号": self.serial_number,
            "管理编号": self.manage_id,
            "批准人": self.approver,
            "核验员": self.inspector,
            "检定员": self.verifier,
            "检校日期": self.check_date.replace("00:00:00",""),
        }

    def is_number(self,s):
        try:
            float(s) if '.' in s else int(s)
            return True
        except ValueError:
            return False

    def filterdian(self,str):
        if self.is_number(str):
            return str.replace(".0","")
        else:
            return str