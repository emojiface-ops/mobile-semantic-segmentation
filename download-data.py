import argparse
import urllib2
import tarfile
import StringIO
import os.path

def download_and_decompress_file(url, person_list, out_path):
    print "Downloading %s, this may take a few minutes..." % url
    response = urllib2.urlopen(url)
    compressedFile = StringIO.StringIO(response.read())

    # Save files in a flat structure
    # Save only .jpg and .ppm files
    outlist = []
    with tarfile.open(fileobj=compressedFile, mode='r:gz') as _tar:
        for member in _tar:
            path = member.name
            extension = os.path.splitext(path)[1]
            if extension != '.jpg' and extension != '.ppm':
                continue

            # Parse filename
            index_of_slash = path.rfind('/')
            if index_of_slash != -1:
                filename = path[path.rfind('/')+1:] # Everything after last '/'
                cleaned_filename = filename
            # Remove '._' at the beginning of some names
            if path.find('._') != -1:
                cleaned_filename = path[path.find('._')+2:]

            person_name = cleaned_filename[0:cleaned_filename.find('.')]
            is_in_list = (person_name in person_list) or person_list == []

            if is_in_list:
                _tar.makefile(member, out_path + '/' + filename)
                outlist.append(person_name)
    return outlist

def download_data(imgs_url, masks_url):
    """
    Downloads data from URLs, then processes it
    Images and masks both go into /downloads folder
    """

    # Download and unzip masks
    person_list = download_and_decompress_file(masks_url, [], 'data/raw/masks')

    # Download and unzip images, saving only images with masks
    download_and_decompress_file(imgs_url, person_list, 'data/raw/images')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--imgs_url',
        type=str,
        default='http://vis-www.cs.umass.edu/lfw/lfw-funneled.tgz',
        help='URL of raw images.'
    )
    parser.add_argument(
        '--masks_url',
        type=str,
        default='http://vis-www.cs.umass.edu/lfw/part_labels/parts_lfw_funneled_gt_images.tgz',
        help='URL of image masks.'
    )

    args, _ = parser.parse_known_args()

    download_data(**vars(args))
