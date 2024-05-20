class ReportDataDatabaseRouter:
    # Hardcoded data variables
    app_label = 'report_data'
    database_name = 'dzsi'

    def db_for_read(self, model, **hints):
        """
        Attempts to read models go to report_db.
        """
        if model._meta.app_label == self.app_label:
            return self.database_name
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write models go to report_db.
        """
        if model._meta.app_label == self.app_label:
            return self.database_name
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the report_data app is involved.
        """
        if obj1._meta.app_label == self.app_label or \
           obj2._meta.app_label == self.app_label:
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the report_data app only appears in the 'report_db'
        database.
        """
        if app_label == self.app_label:
            return db == self.database_name
        return None
