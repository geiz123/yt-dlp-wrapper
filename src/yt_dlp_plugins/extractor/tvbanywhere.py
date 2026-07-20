import json
import re

from yt_dlp.extractor.common import InfoExtractor


class TVBAnywhereIE(InfoExtractor):
    IE_NAME = 'tvbanywhere'

    _VALID_URL = (
        r'https?://(?:www\.)?tvbanywherena\.com/'
        r'(?:[a-z]{2}/)?watch/[^/]+/(?P<id>\d+)'
    )

    _TESTS = [{
        'url': 'https://tvbanywherena.com/vn/watch/3688-The-Map-Of-Truth/1865291940319844006',
        'info_dict': {
            'id': '1865291940319844006',
            'title': 'Tập 01',
        },
        'params': {
            'skip_download': True,
        },
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        # Download TVB page
        webpage = self._download_webpage(url, video_id)

        # Find VideoObject JSON-LD
        json_ld_blocks = re.findall(
            r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            webpage,
            re.DOTALL,
        )

        video_obj = None

        for block in json_ld_blocks:
            try:
                data = json.loads(block)
            except json.JSONDecodeError:
                continue

            if data.get('@type') == 'VideoObject':
                video_obj = data
                break

        if not video_obj:
            self.raise_no_formats(
                'Unable to locate VideoObject',
                expected=True,
            )

        embed_url = video_obj.get('embedUrl')

        if not embed_url:
            self.raise_no_formats(
                'Unable to locate Brightcove embed URL',
                expected=True,
            )

        # Extract account ID
        account_id = self._search_regex(
            r'players\.brightcove\.net/(\d+)/',
            embed_url,
            'account id',
        )

        # Download Brightcove player page
        player_page = self._download_webpage(
            embed_url,
            video_id,
            note='Downloading Brightcove player',
        )

        # Extract policy key
        policy_key = self._search_regex(
            r'policyKey["\']?\s*:\s*["\']([^"\']+)["\']',
            player_page,
            'policy key',
        )

        # Playback API
        playback = self._download_json(
            f'https://edge.api.brightcove.com/playback/v1/accounts/{account_id}/videos/{video_id}',
            video_id,
            headers={
                'Accept': f'application/json;pk={policy_key}',
                'Origin': 'https://tvbanywherena.com',
                'Referer': 'https://tvbanywherena.com/',
            },
        )

        formats = []

        for source in playback.get('sources', []):
            src = source.get('src')

            if not src:
                continue

            source_type = source.get('type')

            if source_type == 'application/x-mpegURL':
                formats.extend(
                    self._extract_m3u8_formats(
                        src,
                        video_id,
                        ext='mp4',
                        fatal=False,
                    )
                )

            elif source_type == 'application/dash+xml':
                formats.extend(
                    self._extract_mpd_formats(
                        src,
                        video_id,
                        fatal=False,
                    )
                )

            elif source.get('container') == 'MP4':
                formats.append({
                    'format_id': 'http',
                    'url': src,
                    'width': source.get('width'),
                    'height': source.get('height'),
                    'filesize': source.get('size'),
                    'tbr': (
                        source.get('avg_bitrate', 0) / 1000
                        if source.get('avg_bitrate')
                        else None
                    ),
                })

        subtitles = {}

        for track in playback.get('text_tracks', []):
            sub_url = track.get('src')

            if not sub_url:
                continue

            lang = track.get('srclang') or 'und'

            subtitles.setdefault(lang, []).append({
                'url': sub_url,
            })

        thumbnails = []

        if playback.get('poster'):
            thumbnails.append({
                'url': playback['poster'],
            })

        return {
            'id': video_id,
            'title': playback.get('name'),
            'description': playback.get('description'),
            'duration': (
                playback.get('duration', 0) / 1000
                if playback.get('duration')
                else None
            ),
            'thumbnails': thumbnails,
            'subtitles': subtitles,
            'formats': formats,
        }