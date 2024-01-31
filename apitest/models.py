from django.db import models


class Administrators(models.Model):
    adminid = models.BigIntegerField(
        db_column="AdminID", primary_key=True
    )  # Field name made lowercase.
    adminname = models.CharField(
        db_column="AdminName", max_length=50
    )  # Field name made lowercase.
    mobileno = models.CharField(
        db_column="MobileNo", max_length=10
    )  # Field name made lowercase.
    adminpassword = models.TextField(
        db_column="AdminPassword"
    )  # Field name made lowercase.
    adminemail = models.CharField(max_length=50, blank=True, null=True)
    firebaseid = models.TextField(db_column="FirebaseID")  # Field name made lowercase.
    fcmtoken = models.TextField(db_column="FCMToken")  # Field name made lowercase.
    deviceinfo = models.TextField(db_column="DeviceInfo")  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=20
    )  # Field name made lowercase.

    class Meta:
        db_table = "administrators"


class Appconfig(models.Model):
    configid = models.AutoField(db_column='ConfigId', primary_key=True)  # Field name made lowercase.
    configname = models.CharField(db_column='ConfigName', max_length=100)  # Field name made lowercase.
    configvalue = models.CharField(db_column='ConfigValue', max_length=500, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'appconfig'


class Businessdetails(models.Model):
    businessid = models.BigIntegerField(
        db_column="BusinessID", primary_key=True
    )  # Field name made lowercase.
    businessname = models.CharField(
        db_column="BusinessName", max_length=50
    )  # Field name made lowercase.
    address = models.TextField(
        db_column="Address", blank=True, null=True
    )  # Field name made lowercase.
    pincode = models.CharField(
        db_column="Pincode", max_length=6, blank=True, null=True
    )  # Field name made lowercase.
    contactno = models.CharField(
        db_column="ContactNo", max_length=50, blank=True, null=True
    )  # Field name made lowercase.
    email = models.CharField(
        db_column="Email", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    geolocation = models.TextField(
        db_column="GeoLocation", blank=True, null=True
    )  # Field name made lowercase.
    marginlength = models.FloatField(
        db_column="MarginLength", blank=True, null=True
    )  # Field name made lowercase.
    marginwidth = models.FloatField(
        db_column="MarginWidth", blank=True, null=True
    )  # Field name made lowercase.
    burstingfactor = models.FloatField(
        db_column="BurstingFactor", blank=True, null=True
    )  # Field name made lowercase.
    gsm = models.FloatField(
        db_column="GSM", blank=True, null=True
    )  # Field name made lowercase.
    rate = models.FloatField(
        db_column="Rate", blank=True, null=True
    )  # Field name made lowercase.
    flutefactor = models.FloatField(
        db_column="FluteFactor"
    )  # Field name made lowercase.
    waste = models.FloatField(db_column="Waste")  # Field name made lowercase.
    conversionrate = models.FloatField(
        db_column="ConversionRate"
    )  # Field name made lowercase.
    profit = models.FloatField(db_column="Profit")  # Field name made lowercase.
    tax = models.FloatField(db_column="Tax")  # Field name made lowercase.
    estimatenote = models.TextField(
        db_column="EstimateNote", blank=True, null=True
    )  # Field name made lowercase.
    activationdate = models.DateField(
        db_column="ActivationDate"
    )  # Field name made lowercase.
    subscriptiondate = models.DateField(
        db_column="SubscriptionDate"
    )  # Field name made lowercase.
    multiuser = models.IntegerField(db_column="Multiuser")  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=10, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "businessdetails"


class Businesses(models.Model):
    businessid = models.BigIntegerField(
        db_column="BusinessID", primary_key=True
    )  # Field name made lowercase.
    authkey = models.CharField(
        db_column="AuthKey", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    serialkey = models.TextField(
        db_column="SerialKey", blank=True, null=True
    )  # Field name made lowercase.
    businessname = models.CharField(
        db_column="BusinessName", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    proprietorname = models.CharField(
        db_column="ProprietorName", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    mobileno = models.CharField(
        db_column="MobileNo", max_length=10, blank=True, null=True
    )  # Field name made lowercase.
    address = models.TextField(
        db_column="Address", blank=True, null=True
    )  # Field name made lowercase.
    businesstype = models.CharField(
        db_column="BusinessType", max_length=20, blank=True, null=True
    )  # Field name made lowercase.
    joiningdate = models.DateField(
        db_column="JoiningDate", blank=True, null=True
    )  # Field name made lowercase.
    expirydate = models.DateField(
        db_column="ExpiryDate", blank=True, null=True
    )  # Field name made lowercase.
    accessdate = models.DateField(
        db_column="AccessDate", blank=True, null=True
    )  # Field name made lowercase.
    remark = models.TextField(
        db_column="Remark", blank=True, null=True
    )  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=20, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "businesses"


class Clientdetails(models.Model):
    clientid = models.BigIntegerField(
        db_column="ClientID", primary_key=True
    )  # Field name made lowercase.
    businessid = models.IntegerField(
        db_column="BusinessID"
    )  # Field name made lowercase.
    clientname = models.CharField(
        db_column="ClientName", max_length=100
    )  # Field name made lowercase.
    mobileno = models.CharField(
        db_column="MobileNo", max_length=10
    )  # Field name made lowercase.
    address = models.TextField(
        db_column="Address", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "clientdetails"


class Developers(models.Model):
    userid = models.IntegerField(
        db_column="UserID", primary_key=True
    )  # Field name made lowercase.
    username = models.CharField(
        db_column="UserName", max_length=20
    )  # Field name made lowercase.
    userpassword = models.TextField(
        db_column="UserPassword"
    )  # Field name made lowercase.
    fullname = models.CharField(
        db_column="FullName", max_length=50
    )  # Field name made lowercase.
    mobileno = models.CharField(
        db_column="MobileNo", max_length=10
    )  # Field name made lowercase.
    userrole = models.CharField(
        db_column="UserRole", max_length=10
    )  # Field name made lowercase.
    members = models.IntegerField(db_column="Members")  # Field name made lowercase.
    reports = models.IntegerField(db_column="Reports")  # Field name made lowercase.
    sms = models.IntegerField(db_column="SMS")  # Field name made lowercase.
    setting = models.IntegerField(db_column="Setting")  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=10
    )  # Field name made lowercase.

    class Meta:
        db_table = "developers"


class Estimatedetails(models.Model):
    estimateid = models.BigIntegerField(
        db_column="EstimateID", primary_key=True
    )  # Field name made lowercase.
    businessid = models.BigIntegerField(
        db_column="BusinessID"
    )  # Field name made lowercase.
    clientid = models.BigIntegerField(
        db_column="ClientID"
    )  # Field name made lowercase.
    userid = models.BigIntegerField(db_column="UserID")  # Field name made lowercase.
    estimatedate = models.DateField(
        db_column="EstimateDate"
    )  # Field name made lowercase.
    boxname = models.CharField(
        db_column="BoxName", max_length=50
    )  # Field name made lowercase.
    length_mm_field = models.FloatField(
        db_column="Length(mm)"
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    width_mm_field = models.FloatField(
        db_column="Width(mm)"
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    height_mm_field = models.FloatField(
        db_column="Height(mm)"
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    length_cm_field = models.FloatField(
        db_column="Length(cm)", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    width_cm_field = models.FloatField(
        db_column="Width(cm)", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    height_cm_field = models.FloatField(
        db_column="Height(cm)", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    length_inch_field = models.FloatField(
        db_column="Length(inch)", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    width_inch_field = models.FloatField(
        db_column="Width(inch)", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    height_inch_field = models.FloatField(
        db_column="Height(inch)", blank=True, null=True
    )  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    ply = models.FloatField(db_column="Ply")  # Field name made lowercase.
    ups = models.FloatField(db_column="Ups")  # Field name made lowercase.
    cuttinglengthmargin = models.FloatField(
        db_column="CuttingLengthMargin"
    )  # Field name made lowercase.
    decalsizemargin = models.FloatField(
        db_column="DecalSizeMargin"
    )  # Field name made lowercase.
    cuttinglength = models.FloatField(
        db_column="CuttingLength"
    )  # Field name made lowercase.
    decalsize = models.FloatField(db_column="DecalSize")  # Field name made lowercase.
    topbf = models.FloatField(db_column="TopBF")  # Field name made lowercase.
    topgsm = models.FloatField(db_column="TopGSM")  # Field name made lowercase.
    toprate = models.FloatField(db_column="TopRate")  # Field name made lowercase.
    f1bf = models.FloatField(db_column="F1BF")  # Field name made lowercase.
    f1gsm = models.FloatField(db_column="F1GSM")  # Field name made lowercase.
    f1rate = models.FloatField(db_column="F1Rate")  # Field name made lowercase.
    f1ff = models.FloatField(db_column="F1FF")  # Field name made lowercase.
    m1bf = models.FloatField(db_column="M1BF")  # Field name made lowercase.
    m1gsm = models.FloatField(db_column="M1GSM")  # Field name made lowercase.
    m1rate = models.FloatField(db_column="M1Rate")  # Field name made lowercase.
    f2bf = models.FloatField(db_column="F2BF")  # Field name made lowercase.
    f2gsm = models.FloatField(db_column="F2GSM")  # Field name made lowercase.
    f2rate = models.FloatField(db_column="F2Rate")  # Field name made lowercase.
    f2ff = models.FloatField(db_column="F2FF")  # Field name made lowercase.
    m2bf = models.FloatField(db_column="M2BF")  # Field name made lowercase.
    m2gsm = models.FloatField(db_column="M2GSM")  # Field name made lowercase.
    m2rate = models.FloatField(db_column="M2Rate")  # Field name made lowercase.
    f3bf = models.FloatField(db_column="F3BF")  # Field name made lowercase.
    f3gsm = models.FloatField(db_column="F3GSM")  # Field name made lowercase.
    f3rate = models.FloatField(db_column="F3Rate")  # Field name made lowercase.
    f3ff = models.FloatField(db_column="F3FF")  # Field name made lowercase.
    bottombf = models.FloatField(db_column="BottomBF")  # Field name made lowercase.
    bottomgsm = models.FloatField(db_column="BottomGSM")  # Field name made lowercase.
    bottomrate = models.FloatField(db_column="BottomRate")  # Field name made lowercase.
    totalgsm = models.FloatField(db_column="TotalGSM")  # Field name made lowercase.
    totalbs = models.FloatField(db_column="TotalBS")  # Field name made lowercase.
    netweight = models.FloatField(db_column="NetWeight")  # Field name made lowercase.
    netpapercost = models.FloatField(
        db_column="NetPaperCost"
    )  # Field name made lowercase.
    waste = models.FloatField(db_column="Waste")  # Field name made lowercase.
    totalweight = models.FloatField(
        db_column="TotalWeight"
    )  # Field name made lowercase.
    totalpapercost = models.FloatField(
        db_column="TotalPaperCost"
    )  # Field name made lowercase.
    conversionrate = models.FloatField(
        db_column="ConversionRate"
    )  # Field name made lowercase.
    overheadcharges = models.FloatField(
        db_column="OverheadCharges"
    )  # Field name made lowercase.
    boxcost = models.FloatField(db_column="BoxCost")  # Field name made lowercase.
    profit = models.FloatField(db_column="Profit")  # Field name made lowercase.
    boxprice = models.FloatField(db_column="BoxPrice")  # Field name made lowercase.
    tax = models.FloatField(db_column="Tax")  # Field name made lowercase.
    boxpricewithtax = models.FloatField(
        db_column="BoxPriceWithTax"
    )  # Field name made lowercase.
    comment = models.CharField(
        db_column="Comment", blank=True, max_length=100, null=True
    )  # Field name made lowercase.
    
    class Meta:
        db_table = "estimatedetails"


class Plydetails(models.Model):
    plyid = models.BigIntegerField(
        db_column="PlyID", primary_key=True
    )  # Field name made lowercase.
    businessid = models.BigIntegerField(
        db_column="BusinessID"
    )  # Field name made lowercase.
    boxid = models.BigIntegerField(db_column="BoxID")  # Field name made lowercase.
    plyno = models.BigIntegerField(db_column="PlyNo")  # Field name made lowercase.
    plyname = models.CharField(
        db_column="PlyName", max_length=50
    )  # Field name made lowercase.
    burstingfactor = models.FloatField(
        db_column="BurstingFactor"
    )  # Field name made lowercase.
    gsm = models.FloatField(db_column="GSM")  # Field name made lowercase.
    rate = models.FloatField(db_column="Rate")  # Field name made lowercase.
    flutefactor = models.FloatField(
        db_column="FluteFactor"
    )  # Field name made lowercase.
    weight = models.FloatField(db_column="Weight")  # Field name made lowercase.
    cost = models.FloatField(db_column="Cost")  # Field name made lowercase.
    burstingstrength = models.FloatField(
        db_column="BurstingStrength"
    )  # Field name made lowercase.

    class Meta:
        db_table = "plydetails"


class Subscriptiondetails(models.Model):
    subscriptionid = models.BigIntegerField(
        db_column="SubscriptionID", primary_key=True
    )  # Field name made lowercase.
    subscription = models.CharField(
        db_column="Subscription", max_length=50
    )  # Field name made lowercase.
    duration = models.IntegerField(db_column="Duration")  # Field name made lowercase.
    amount = models.FloatField(db_column="Amount")  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=10, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "subscriptiondetails"


class Transactiondetails(models.Model):
    transactionid = models.BigIntegerField(
        db_column="TransactionID", primary_key=True
    )  # Field name made lowercase.
    businessid = models.BigIntegerField(
        db_column="BusinessID"
    )  # Field name made lowercase.
    transactiondate = models.DateField(
        db_column="TransactionDate"
    )  # Field name made lowercase.
    duration = models.IntegerField(db_column="Duration")  # Field name made lowercase.
    amount = models.FloatField(db_column="Amount")  # Field name made lowercase.
    perticulars = models.TextField(
        db_column="Perticulars", blank=True, null=True
    )  # Field name made lowercase.
    status = models.TextField(
        db_column="Status", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "transactiondetails"


class Userdetails(models.Model):
    userid = models.BigIntegerField(
        db_column="UserID", primary_key=True
    )  # Field name made lowercase.
    businessid = models.BigIntegerField(
        db_column="BusinessID"
    )  # Field name made lowercase.
    userpassword = models.TextField(
        db_column="UserPassword"
    )  # Field name made lowercase.
    username = models.CharField(
        db_column="UserName", max_length=50
    )  # Field name made lowercase.
    mobileno = models.CharField(
        db_column="MobileNo", max_length=10
    )  # Field name made lowercase.
    userrole = models.CharField(
        db_column="UserRole", max_length=50
    )  # Field name made lowercase.
    useraccess = models.IntegerField(
        db_column="UserAccess"
    )  # Field name made lowercase.
    androidid = models.CharField(
        db_column="AndroidID", max_length=100, blank=True, null=True
    )  # Field name made lowercase.
    deviceinfo = models.TextField(
        db_column="DeviceInfo", blank=True, null=True
    )  # Field name made lowercase.
    status = models.CharField(
        db_column="Status", max_length=10, blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        db_table = "userdetails"
