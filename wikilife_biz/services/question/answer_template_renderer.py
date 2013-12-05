# coding=utf-8

YES = "yes"
NO = "no"


class AnswerTemplateRendererException(Exception):
    pass


class AnswerTemplateRenderer(object):
    """
    Evaluates a boolean expression
    """

    def render(self, template, value_str):
        """
        template: String
        value_str: String

        Returns: String
        """

        def v():
            return value_str

        def v_capitalize():
            return value_str.capitalize()

        def v_lower():
            return value_str.lower()

        def v_tyn(yes_value, no_value, other_to_lower=False):
            value_str_lower = value_str.lower()

            if value_str_lower == YES:
                return yes_value
            elif value_str_lower == NO:
                return no_value
            elif other_to_lower:
                return value_str_lower
            else:
                return value_str

        def v_tyn_lower(yes_value, no_value):
            return v_tyn(yes_value, no_value, True)

        try:
            r = str(eval(template))
            r = " ".join(r.split())  # remove extra blanks
            return r

        except Exception, e:
            print "ERROR: '%s' render('%s', '%s')" % (e, template, value_str)
            raise
