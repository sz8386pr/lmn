import logging

def delete_photo(photo):
    logging.info('to do : delete photo at url %s' % photo)
    photo.delete()
