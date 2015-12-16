from Products.Five import BrowserView
# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ProjectOverviewView(BrowserView):

    def prepprojects(self):
        """ collect projects """
        contents = self.context.getFolderContents(
            {'portal_type': 'Folder',
             'sort_on': 'getObjPositionInParent'},
            batch=True,
            b_size=100)

        projects = []

        for folder in contents:
            imgs = folder.getObject().getFolderContents(
                {'portal_type': 'Image', 'sort_on': 'getObjPositionInParent'},
                batch=True, b_size=100)
            imgobs = []
            for img in imgs:
                imgob = img.getObject()
                imgobs.append(imgob)
                width, height = imgob.image.getImageSize()
                width = int(160.0 / height * width)
                projects.append(
                    dict(id=folder.getId,
                         title=folder.Title,
                         imgs=imgobs,
                         width=width))

        return projects
