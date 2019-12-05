class SQL:

    def __init__(self, **kwargs):
        self.sql_type = kwargs['sql_type']
        self.table = kwargs['table']
        self.columns = sorted(kwargs['columns'])
        self.str_form = ''

        if 'where' in kwargs.keys():
            self.where = kwargs['where']
        else:
            self.where = None
        self.makeIntoSQL()

    def makeIntoSQL(self):
        str_form = ''
        if self.sql_type == 'insert':
            str_form += 'insert into ' + self.table + ' '
            tmp = ', '.join(self.columns)
            str_form += '(' + tmp + ') values('
            values_tmp = ['%s' for x in range(len(self.columns))]
            tmp = ', '.join(values_tmp)
            str_form += tmp + ')'
        elif self.sql_type == 'select':
            str_form += 'select '
            tmp = ', '.join(self.columns)
            str_form += tmp + ' '
            str_form += 'from ' + self.table

            if self.where is not None:
                str_form += ' where ' + self.where

        self.str_form = str_form

    @classmethod
    def sort_args(cls, record):
        return [e[1] if e[1] != '' else None for e in sorted(record.items(), key=lambda x: x[0])]

    def __str__(self):
        return self.str_form
