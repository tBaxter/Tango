import time
import zipfile

from .models import GalleryImage

def process_upload(photo_list, form, user, status=''):
    """
    Helper function that actually processes and saves the upload(s).
    Segregated out for readability.
    """
    caption = contact_address = contact_city = contact_phone = ''
    status += "beginning upload processing. Gathering and normalizing fields....<br>"

    for upload_file in photo_list:
        upload_file.name = upload_file.name.lower().replace(' ', '_')  # lowercase and replace spaces
        upload_name = upload_file.name

        status += "File is %s. Checking for single file upload or bulk upload... <br>" % upload_name
        if upload_name.endswith('.jpg') or upload_name.endswith('.jpeg'):
            status += "Found jpg. Attempting to save... <br>"
            # to do: proper dupe checking
            dupe = False
            if not dupe:
                upload = Upload(
                    gallery_form    = controller,
                    sender_name     = form.cleaned_data['name'],
                    sender_email    = form.cleaned_data['from_address'],
                    photo           = upload_file,
                    contact_address = contact_address,
                    caption         = caption
                )
                upload.save()
                time.sleep(1)
                status += "Saved and uploaded jpg."
            #except Exception, inst:
            #    status += "Error saving image: %s" % (inst)

        elif upload_name.endswith('.zip'):
            """
            We're going to do a bulk upload.
            For reference, see the gallery app or
            http://code.google.com/p/django-photologue/source/browse/trunk/photologue/models.py#194
            Also note use of custom storage. See: http://docs.djangoproject.com/en/dev/topics/files/
            """
            status += "Found zip. Attempting to process. <br>"
            from django.core.files.base import ContentFile
            from cStringIO import StringIO

            working_zip = zipfile.ZipFile(upload_file)
            status += "have working zip. Filelist is %s <br>" % str(working_zip.namelist())
            bad_file = working_zip.testzip()
            if bad_file:
                status += '"%s" in the .zip archive is corrupt.<br>' % bad_file
                raise Exception('"%s" in the .zip archive is corrupt.' % bad_file)

            for filename in working_zip.namelist():
                if filename.startswith('__'):  # do not process meta files
                    continue
                if not filename.lower().endswith('.jpg'):  # bail if it's not jpg
                    continue
                status += "beginning processing %s ... " % filename

                data = working_zip.read(filename)
                if len(data):
                    status += "we have data. Attempting to test for validity <br> "
                    # test for truncated and broken images
                    try:
                        trial_image = Image.open(StringIO(data))
                        trial_image.load()
                    except Exception:
                        continue
                    filename = filename.replace(' ','_').replace('#','').replace('/','_')
                    # test for dupes
                    try:
                        full_filename = 'uploaded/%s/%s/%s' % (datetime.datetime.today().year, controller.slug, filename)
                        dupe = Upload.objects.get(photo=full_filename, controller=controller)
                    except:
                        if not ContentFile(data):
                           return filename                    
                    path = SimpleUploadedFile('uploaded/'+filename, data)
                    upload = Upload(
                        gallery_form    = controller,
                     sender_name     = form.cleaned_data['name'],
                     photo           = path,
                     caption         = caption,   
                )
                if faces:
                    upload.sellable = True
                    upload.faces    = True
                upload.save()
                time.sleep(.5)  # give a little breathing room for the server 
            working_zip.close()
            status += "bulk upload completed"
    return status
