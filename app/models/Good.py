import uuid
from app import db
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime


class Good(db.Model, UserMixin):
    __tablename__ = 'SHOP_GOOD'

    ID = db.Column(db.String(50), primary_key=True, nullable=False, comment="ID")
    CREATE_DATETIME = db.Column(db.DateTime, index=True, default=datetime.now(), nullable=False, comment="创建时间")
    BRAND = db.Column(db.String(150), nullable=False, default="", comment="品牌")
    COLOR = db.Column(db.String(30), nullable=False, default="", comment="颜色")
    STYLE = db.Column(db.String(50), nullable=False, default="", comment="款式")
    DESCRIPTION = db.Column(db.Text, nullable=False, default="", comment="描述")
    SUPPLIER_COLOR = db.Column(db.String(30), nullable=False, default="", comment="供应商配色")
    MATERIAL = db.Column(db.String(255), nullable=False, default="", comment="材质")
    PLACE_OF_ORIGIN = db.Column(db.String(255), nullable=False, default="", comment="产地")
    PRODUCT_NUMBER = db.Column(db.String(50), nullable=False, default="", comment="产品编号")
    FACTORY_CODE = db.Column(db.String(40), nullable=False, default="", comment="工厂代码")
    AREA_ID = db.Column(db.String(50), db.ForeignKey('SHOP_AREA.ID', ondelete='SET NULL'), comment="地区ID")
    CURRENCY = db.Column(db.String(50), nullable=False, default="", comment="货币")
    CATEGORY_ID = db.Column(db.String(50), db.ForeignKey('SHOP_GOOD_CATEGORY.ID',
                                                         ondelete='SET NULL'), comment="产品分类ID")
    SIZE = db.Column(db.String(255), nullable=False, default="", comment="尺码")
    SIZE_CHART = db.Column(db.String(255), nullable=False, default="", comment="尺码表地址")
    STAFF_EMAIL = db.Column(db.String(50), nullable=False, default="", comment="员工邮箱")

    def __repr__(self):
        return '<Good %r>\n' % self.NAME

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'NAME': self.NAME,
            'DESCRIPTION': self.DESCRIPTION,
        }
