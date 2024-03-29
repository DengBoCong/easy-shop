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
    CATEGORY = db.Column(db.String(100), nullable=False, default="", comment="产品分类")
    CATEGORY_ID = db.Column(db.String(50), db.ForeignKey('SHOP_GOOD_CATEGORY.ID',
                                                         ondelete='SET NULL'), comment="产品分类ID")
    SIZE = db.Column(db.String(255), nullable=False, default="", comment="尺码")
    SIZE_CHART = db.Column(db.String(255), nullable=False, default="", comment="尺码表地址")
    STAFF_EMAIL = db.Column(db.String(50), nullable=False, default="", comment="员工邮箱")
    IS_PUBLISHED = db.Column(db.Boolean, nullable=False, default=True, comment="是否发布")
    CLASS = db.Column(db.Enum('SAMPLE', 'DESIGN', 'REFERENCE'), nullable=False, comment="产品归类")
    TYPE = db.Column(db.Enum('MEN', 'WOMEN', 'KIDS', 'OTHERS'), nullable=False, comment="所属类型")
    COVER = db.Column(db.String(255), nullable=False, default="", comment="封面地址")
    USER_ID = db.Column(db.String(50), db.ForeignKey('SHOP_USER.ID', ondelete='SET NULL'), comment="USER ID")
    NUM = db.Column(db.Integer, nullable=False, default=0, comment="数量")  # 销量
    PRICE = db.Column(db.DECIMAL(20, 3), nullable=False, default=0.000, comment="价格")

    orderGoods = db.relationship('OrderGood', backref='good', lazy='dynamic')
    goodPrices = db.relationship('GoodPrice', backref='good', lazy='dynamic')
    wishGoods = db.relationship('WishGood', backref='good', lazy='dynamic')
    shoppingGoods = db.relationship('ShoppingGood', backref='good', lazy='dynamic')
    sampleGoods = db.relationship('SampleGood', backref='good', lazy='dynamic')

    def __repr__(self):
        return '<Good %r>\n' % self.ID

    def to_json(self):
        return {
            'ID': self.ID,
            'CREATE_DATETIME': self.CREATE_DATETIME.strftime('%Y-%m-%d %H:%M:%S'),
            'BRAND': self.BRAND,
            'COLOR': self.COLOR,
            'STYLE': self.STYLE,
            'DESCRIPTION': self.DESCRIPTION,
            'SUPPLIER_COLOR': self.SUPPLIER_COLOR,
            'MATERIAL': self.MATERIAL,
            'PLACE_OF_ORIGIN': self.PLACE_OF_ORIGIN,
            'PRODUCT_NUMBER': self.PRODUCT_NUMBER,
            'FACTORY_CODE': self.FACTORY_CODE,
            'AREA_ID': self.AREA_ID,
            'CURRENCY': self.CURRENCY,
            'CATEGORY': self.CATEGORY,
            'CATEGORY_ID': self.CATEGORY_ID,
            'SIZE': self.SIZE,
            'SIZE_CHART': self.SIZE_CHART,
            'STAFF_EMAIL': self.STAFF_EMAIL,
            'IS_PUBLISHED': self.IS_PUBLISHED,
            'CLASS': self.CLASS,
            'TYPE': self.TYPE,
            'COVER': self.COVER,
            'USER_ID': self.USER_ID,
            'NUM': self.NUM,
            'PRICE': self.PRICE
        }
