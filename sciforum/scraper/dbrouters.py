class MongoRouter:
    """
    A router to control all database operations on models in the
    scraper applications.
    """
    route_app_labels = {'event', 'webinar', 'scraper'}

    def db_for_read(self, model, **hints):
        """
        Attempts to read events and webinars models go to crawler db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'crawler'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Attempts to write events and webinars models go to crawler db.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'crawler'
        return 'default'

    '''def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the events or webinars apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or
            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return True'''

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the events and webinars apps only appear in the
        'auth_db' database.
        """
        if app_label in self.route_app_labels:
            return db == 'crawler'
        return None