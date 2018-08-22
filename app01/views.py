from django.shortcuts import render,redirect
from app01 import models
from django.forms import Form,ModelForm
from django.forms import fields
from django.forms import widgets

# Create your views here.


class TestForm(Form):
    user = fields.CharField()
    email = fields.EmailField()
    ug = fields.ChoiceField(
        widget=widgets.Select,
        choices=[]
    )

    def __init__(self,*args,**kwargs):
        super(TestForm,self).__init__(*args,**kwargs)
        self.fields["ug"].choices = models.UserGroup.objects.values_list("id","title")


class TestModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        error_messages = {
            "user":{"required":"用户名不能为空"},
            "email":{"required":"邮箱不能为空","invalid":"邮箱格式错误"},
        }


def test(request):
    if request.method == "GET":
        form = TestModelForm()
        context = {
            "form":form,
        }
        return render(request,"test.html",context)
    else:
        form = TestModelForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("http://www.baidu.com")
        context = {
            "form": form,
        }
        return render(request, "test.html", context)


def edit(request,nid):
    obj = models.UserInfo.objects.filter(id=nid).first()
    if request.method == "GET":
        form = TestModelForm(instance=obj)
        context = {
            "form": form,
        }
        return render(request, "edit.html", context)
    else:
        form = TestModelForm(instance=obj,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("http://www.baidu.com")
        context = {
            "form": form,
        }
        return render(request, "edit.html", context)

