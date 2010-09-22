from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import login
from zope.configuration import xmlconfig
from plone.app.testing.layers import FunctionalTesting
from plone.testing import z2


class PACollection(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import plone.app.collection
        xmlconfig.file('configure.zcml', plone.app.collection,
                       context=configurationContext)
        z2.installProduct(app, 'plone.app.collection')

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'plone.app.collection:default')

        # create admin user
        # z2.setRoles(portal, TEST_USER_NAME, ['Manager']) does not work
        # setRoles(portal, TEST_USER_NAME, ['Manager']) is not working either
        portal.acl_users.userFolderAddUser('admin',
                                           'secret',
                                           ['Manager'],
                                           [])
        login(portal, 'admin')

        # enable workflow for browser tests
        workflow = portal.portal_workflow
        workflow.setDefaultChain('plone_workflow')

        # add a page, so we can test with it
        portal.invokeFactory("Document",
                             "collectiontestpage",
                             title="Collection Test Page")
        workflow.doActionFor(portal.collectiontestpage, "publish")

        # add a collection, so we can add a query to it
        portal.invokeFactory("Collection",
                             "collection",
                             title="New Collection")
        workflow.doActionFor(portal.collection, "publish")


PACOLLECTION_FIXTURE = PACollection()

PACOLLECTION_FUNCTIONAL_TESTING =\
                            FunctionalTesting(bases=(PACOLLECTION_FIXTURE,),
                                              name="PACollection:Functional")
