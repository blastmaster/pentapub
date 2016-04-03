# pentapub - automate the pentaradio publishing

The goal of this project is to provide an automatism to publish pentaradio
episodes.

Beware! This is a work in progress project. The code may change heavily and quickly.

## The Process

Here I made the assumption that you already have a wav of the episode in the
correct form.

Publishing a pentaradio includes the following steps:

* upload the episode to Auphonic
* choose the pentaradio preset, insert title and date
* download the chapter marks from shonot.es
* upload chapter marks to auphonic
* start production, ...download final episodes when finished
* upload episodes to ftp
* adjust resource entry on c3d2.de
* convert chaptermarks to podlove-simple-chapters
* add chapter marks on c3d2.de

## License

pentapub is distributed under the Gnu General Public License (GPL). See the LICENSE
for the full license text.
