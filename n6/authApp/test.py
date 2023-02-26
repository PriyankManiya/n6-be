# from rest_framework.serializers import ModelSerializer, ModelSerializerOptions
#
# class CustomErrorMessagesModelSerializerOptions(ModelSerializerOptions):
#     """
#     Meta class options for CustomErrorMessagesModelSerializerOptions
#     """
#     def __init__(self, meta):
#         super(CustomErrorMessagesModelSerializerOptions, self).__init__(meta)
#         self.error_messages = getattr(meta, 'error_messages', {})
#
# class CustomErrorMessagesModelSerializer(ModelSerializer):
#     _options_class = CustomErrorMessagesModelSerializerOptions
#
#     def __init__(self, *args, **kwargs):
#         super(CustomErrorMessagesModelSerializer, self).__init__(*args, **kwargs)
#
#         # Run through all error messages provided in the Meta class and update
#         for field_name, err_dict in self.opts.error_messages.iteritems():
#             self.fields[field_name].error_messages.update(err_dict)