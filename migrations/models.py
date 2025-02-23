from src.app.auth.artists.models import (  # noqa: F401
    ArtistProfile,
    artists_to_tags_association,
    followers_to_artists_association,
    artists_to_tracks_association,
    artist_to_squad_association,
    album_to_artist_association,
)
from src.app.auth.producers.models import (  # noqa: F401
    ProducerProfile,
    producers_to_squads_association,
    producer_to_beat_association,
    user_to_producer_association,
    producers_to_tags_association,
    producers_to_soundkits_association,
    producers_to_beatpacks_association,
    followers_to_producers_association,
)
from src.app.auth.users.models import (  # noqa: F401
    User,
    user_to_tag_association,
    saver_to_albums_association,
    user_to_artist_association,
    author_to_licenses_association,
    saver_to_playlists_association,
    author_to_playlists_association,
    follower_to_squads_association,
    followers_to_producers_association,
    followers_to_artists_association,
    user_to_producer_association,
)
from src.app.music.albums.interfaces.da.models import (  # noqa: F401
    Album,
    album_to_artist_association,
    album_to_tag_association,
    album_to_track_association,
)
from src.app.music.beatpacks.models import (  # noqa: F401
    Beatpack,
    beatpacks_to_tags_association,
    beatpack_to_beats_association,
    producers_to_beatpacks_association,
)
from src.app.music.beats.models import (  # noqa: F401
    Beat,
    tag_to_beat_association,
    producer_to_beat_association,
)
from src.app.music.soundkits.models import (  # noqa: F401
    Soundkit,
    tag_to_soundkits_association,
    beat_to_soundkits_association,
    producers_to_soundkits_association,
)
from src.app.music.squads.models import (  # noqa: F401
    Squad,
    artist_to_squad_association,
    follower_to_squads_association,
    producers_to_squads_association,
)
from src.app.music.tracks.models import (  # noqa: F401
    Track,
    track_to_tag_association,
    track_to_producer_association,
    user_to_tracks_likes,
    track_to_artist_association,
)
from src.app.social.chats.models import (  # noqa: F401
    Chat,
    messages_to_chat_association,
    user_to_chat_association,
)
from src.app.social.comments.models import (  # noqa: F401
    Comment,
    user_to_comments_association,
)
from src.app.social.licenses.models import (  # noqa: F401
    License,
    author_to_licenses_association,
)
from src.app.social.messages.models import (  # noqa: F401
    Message,
    author_to_messages_association,
    messages_to_chat_association,
)
from src.app.social.notifications.models import (  # noqa: F401
    Notification,
)
from src.app.social.playlists.models import (  # noqa: F401
    Playlist,
    playlists_to_tag_association,
    playlists_to_track_association,
    author_to_playlists_association,
    playlists_to_beat_association,
)
from src.app.social.tags.models import (  # noqa: F401
    Tag,
)
