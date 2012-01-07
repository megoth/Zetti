from django.db import models

class ReportType(models.Model):
	name = models.CharField(max_length=200)
	start_hour = models.PositiveSmallIntegerField(max_length=2)
	start_onethousand = models.PositiveSmallIntegerField(max_length=3)
	start_fivehundred = models.PositiveSmallIntegerField(max_length=3)
	start_twohundred = models.PositiveSmallIntegerField(max_length=3)
	start_onehundred = models.PositiveSmallIntegerField(max_length=3)
	start_fifty = models.PositiveSmallIntegerField(max_length=3)
	start_twenty = models.PositiveSmallIntegerField(max_length=3)
	start_ten = models.PositiveSmallIntegerField(max_length=3)
	start_five = models.PositiveSmallIntegerField(max_length=3)
	start_one = models.PositiveSmallIntegerField(max_length=3)
	start_half = models.PositiveSmallIntegerField(max_length=3)
	
	def __unicode__(self):
		return self.name

class Report(models.Model):
	year = models.PositiveIntegerField(max_length=4)
	report_id = models.PositiveIntegerField()
	report_type = models.ForeignKey(ReportType)
	start_datetime = models.DateTimeField()
	settle_datetime = models.DateTimeField(null=True)
	end_datetime = models.DateTimeField(null=True)
	verified_datetime = models.DateTimeField(null=True)
	sale_high_tax = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	sale_mid_tax = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	sale_no_tax = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	payment_card = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	payment_cash = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	payment_bong = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	other_membership = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	wastage = models.DecimalField(default=0, decimal_places=1, max_digits=5)
	start_onethousand = models.PositiveSmallIntegerField(max_length=3)
	start_fivehundred = models.PositiveSmallIntegerField(max_length=3)
	start_twohundred = models.PositiveSmallIntegerField(max_length=3)
	start_onehundred = models.PositiveSmallIntegerField(max_length=3)
	start_fifty = models.PositiveSmallIntegerField(max_length=3)
	start_twenty = models.PositiveSmallIntegerField(max_length=3)
	start_ten = models.PositiveSmallIntegerField(max_length=3)
	start_five = models.PositiveSmallIntegerField(max_length=3)
	start_one = models.PositiveSmallIntegerField(max_length=3)
	start_half = models.PositiveSmallIntegerField(max_length=3)
	end_onethousand = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_fivehundred = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_twohundred = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_onehundred = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_fifty = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_twenty = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_ten = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_five = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_one = models.PositiveSmallIntegerField(max_length=3, default=0)
	end_half = models.PositiveSmallIntegerField(max_length=3, default=0)
	
	def get_other_total(self):
		return self.other_membership
	
	def get_payment_total(self):
		return (self.payment_card
			+ self.payment_cash
			+ self.payment_bong)
	
	def get_result_conting(self):
		return (self.get_result_value('onethousand', 1000.0)
			+ self.get_result_value('fivehundred', 500.0)
			+ self.get_result_value('twohundred', 200.0)
			+ self.get_result_value('onehundred', 100.0)
			+ self.get_result_value('fifty', 50.0)
			+ self.get_result_value('twenty', 20.0)
			+ self.get_result_value('ten', 10.0)
			+ self.get_result_value('five', 5.0)
			+ self.get_result_value('one', 1.0)
			+ self.get_result_value('half', 0.5))
	
	def get_result_value(self, valuename, value):
		return (vars(self)['end_%s' % valuename] - vars(self)['start_%s' % valuename]) * value
	
	def get_sale_total(self):
		return (self.sale_high_tax
			+ self.sale_mid_tax
			+ self.sale_no_tax)
	
	def get_wastage_level(self):
		wastage = self.get_wastage_total()
		sale = self.get_sale_total()
		return wastage if sale == 0 else wastage / sale * 100
	
	def get_wastage_total(self):
		return (self.get_sale_total()
			- self.get_payment_total())
	
	def update_result_values(self):
		self.__dict__.update({
			'result_onethousand': self.get_result_value('onethousand', 1000.0),
			'result_fivehundred': self.get_result_value('fivehundred', 500.0),
			'result_twohundred': self.get_result_value('twohundred', 200.0),
			'result_onehundred': self.get_result_value('onehundred', 100.0),
			'result_fifty': self.get_result_value('fifty', 50.0),
			'result_twenty': self.get_result_value('twenty', 20.0),
			'result_ten': self.get_result_value('ten', 10.0),
			'result_five': self.get_result_value('five', 5.0),
			'result_one': self.get_result_value('one', 1.0),
			'result_half': self.get_result_value('half', 0.5),
			'result_counting': self.get_result_conting(),
			'sale_total': self.get_sale_total(),
			'payment_total': self.get_payment_total(),
			'other_total': self.get_other_total(),
			'wastage_total': self.get_wastage_total(),
			'wastage_level': self.get_wastage_level(),
		})
