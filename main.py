import environment_processor
import land_processor
import osm_downloader
import way_processor


def main(place, directory, force):
    osm_downloader.main(place, directory, force)

    way_processor.main(directory)

    environment_processor.main(directory)

    land_processor.main(directory)


if __name__ == '__main__':
    Place = 'Seoul'
    Directory = 'Seoul'
    Force = False

    print(f'Place:{Place}')
    print(f'Directory:{Directory}')
    print(f'Force:{Force}')

    main(Place, Directory, Force)
