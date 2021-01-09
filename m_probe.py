from shlex import join
from json import loads

from libs import args, call
import m_audio, m_video

exts = [ m_audio.ext, m_video.ext ]


def process(file):
   file['ac'] = file['vc'] = None

   print( ' ? ', file['path'] )
   stdout = call([ 'ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', str(file['path']) ])

   for c in loads(stdout)['streams']:
      type = c.get( 'codec_type', '' )
      name = c.get( 'codec_name', '' )
      rate = c.get( 'bit_rate',   '9999999')

      if type == 'audio':
         file['ac'] = ( name, int(rate) )
      elif type == 'video' and name not in ['mjpeg', 'png']:
         file['vc'] = ( name, int(rate) )

   if not file['ac'] and file['path'].suffix == m_audio.ext:
      raise Exception('BAD Audio:', file['path'].relative_to(args.dir))

   if not file['vc'] and file['path'].suffix == m_video.ext:
      raise Exception('BAD Video:', file['path'].relative_to(args.dir))

   file['pt'] = file['mt']
