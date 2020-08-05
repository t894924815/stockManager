import datetime
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

# Create your models here.

class Operation(models.Model):
    class Meta:
        verbose_name = '交易记录'
        verbose_name_plural = '交易记录'
    class platformType(models.TextChoices):
        SH = 'sh', _('沪')
        SZ = 'sz',_('深')
    class operationType(models.TextChoices):
        BUY = 'BUY', _('买入')
        SELL = 'SELL', _('卖出')
        Divident = 'DV', _('除权除息')
        
    code = models.CharField(max_length=200,verbose_name='股票代码')
    platformType = models.CharField(max_length=2, choices=platformType.choices,
                                     default=platformType.SH,verbose_name='交易所')
    date = models.DateField(verbose_name='日期')
    operationType = models.CharField(max_length=4,choices=operationType.choices,
        default=operationType.BUY,verbose_name='操作类型') 
    price = models.FloatField(default=0,verbose_name='价格')
    count = models.IntegerField(default=0,blank=True,verbose_name='数量')
    fee = models.FloatField(default=0,verbose_name='手续费')
    comment = models.CharField(max_length=200,blank=True,verbose_name='备注')
    cash = models.FloatField(default=0,verbose_name='分红')  #分红
    stock = models.FloatField(default=0,verbose_name='送股')  #送股
    reserve = models.FloatField(default=0,verbose_name='派股')  #派股

    def __str__(self):
        return self.platformType + self.code+" "+str(self.date)+" "+self.operationType+" "+str(self.count)

    def to_dict(self):
        to_return = {}
        to_return['date'] = str(self.date)
        to_return['type'] = self.operationType
        to_return['price'] = self.price
        to_return['count'] = self.count
        to_return['fee'] = self.fee
        if self.operationType == 'BUY' or self.operationType == 'SELL':
            to_return['sum'] = self.price * self.count
        elif self.operationType == 'DV':
            to_return['sum'] = self.cash * self.count

        if self.operationType == 'DV':
            comment = ''
            if self.cash > 0.0:
                comment += '每10股股息'+ '%.2f' % (self.cash * 10) 
            if self.reserve > 0.0:
                comment += ',每10股转增'+ '%.2f' % (self.reserve * 10) 
            if self.stock > 0.0:
                comment += ',每10股送股'+ '%.2f' % (self.stock * 10) 
            
            to_return['comment'] = comment
        return to_return

class Securities(models.Model):
    class Meta:
        verbose_name = '券商'
        verbose_name_plural = '券商'

    class operationType(models.TextChoices):
        BUY = 'BUY', _('买入')
        SELL = 'SELL', _('卖出')

    name = models.CharField(max_length=200, blank=True, verbose_name='名称')
    operationType = models.CharField(max_length=4,choices=operationType.choices,
        default=operationType.BUY,verbose_name='操作类型')
    commissionRate = models.FloatField(default=0, verbose_name='佣金比率(%)')
    commission = models.FloatField(default=0, verbose_name='佣金最低金额')
    transfer = models.FloatField(default=0, verbose_name='过户费(%)')
    stamp = models.FloatField(default=0, verbose_name='印花税(%)')
    other = models.FloatField(default=0, verbose_name='其他(%)')

    def __str__(self):
        return self.name + " " + self.operationType
