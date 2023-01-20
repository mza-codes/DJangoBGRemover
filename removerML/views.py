from django.shortcuts import render, HttpResponse
from django.core.files.storage import FileSystemStorage
import os, datetime, base64
from . import remover

extensions = ['.jpg', '.jpeg', '.png']

def index(request):
    
    if request.method == 'POST' and request.FILES['image']:
        print(request.FILES)
        print("Inside True STATE")

        image = request.FILES['image']
        ext = os.path.splitext(image.name)[1]
        if ext.lower() in extensions:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            file_name = uploaded_file_url.split("/")[2]

            input_path = os.getcwd() + uploaded_file_url
            output_path = os.getcwd() + "/uploads/" + file_name.split(".")[0] + "_processed.png"

            remover.process(input_path, output_path)
            image_path = uploaded_file_url.split(".")[0] + "_processed.png"
            return render(request, 'removerML/index.html', {"image_path": image_path})
        else:
            # return HttpResponse("Only Allowed extensions are {}".format(extensions))
            msg = "Only Allowed Extensions are {}".format(extensions)
            return render(request, 'removerML/index.html', {"err_msg": msg})
    return render(request, 'removerML/index.html')

def data(request):
    if request.method == 'POST' and request.POST['image']:
        print("Inside True STATE")
        image = request.POST['image']
        data = base64.b64decode(image)
        image_name = datetime.datetime.now().strftime("%Y%b%d%H%M%S%f") + ".jpg"
        image_path = os.getcwd() + "/uploads/" + image_name

        with open(image_path, "wb") as f:
            f.write(data)

        input_path = os.getcwd() + "/uploads/" + image_name
        output_path = os.getcwd() + "/uploads/" + image_name.split(".")[0] + "_processed.png"

        remover.process(input_path, output_path)
        image_path = "/uploads/" + image_name.split(".")[0] + "_processed.png"
        print("Final IMAGE PATH",image_path)
        return HttpResponse(request.get_host() + image_path)

def populate(request):
    if request.method == 'POST' and request.FILES['image']:
        print(request.FILES)
        print("Inside True STATE",)
        image = request.FILES['image']
        ext = os.path.splitext(image.name)[1]
        if ext.lower() in extensions:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            file_name = uploaded_file_url.split("/")[2]

            input_path = os.getcwd() + uploaded_file_url
            output_path = os.getcwd() + "/uploads/" + file_name.split(".")[0] + "_processed.png"

            remover.process(input_path, output_path)
            image_path = uploaded_file_url.split(".")[0] + "_processed.png"
            # return render(request, 'removerML/index.html', {"image_path": image_path})
            response = request.get_host() + image_path
            print(response)

            # data = serializers.serialize('json', response)
            return HttpResponse(response, content_type='application/json')
            # return HttpResponse(request.get_host() + image_path)
        else:
            return HttpResponse("Only Allowed extensions are {}".format(extensions))
    return render(request, 'removerML/index.html')
