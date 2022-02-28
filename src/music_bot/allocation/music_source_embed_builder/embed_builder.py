from __future__ import annotations

import typing
import random

from hikari import Embed, Color

from music_bot.utils.discord import (
    format_datetime,
)
from music_bot.utils.string import (
    convert_optional_string,
    shorten,
)


if typing.TYPE_CHECKING:
    from music_source.track_models import Track


class MusicSourceEmbedBuilder():
    def __init__(self, track: Track) -> None:
        self.track = track

    def get_embed(self) -> Embed:
        track = self.track

        randomizer = random.Random(track.id_)

        embed = Embed(
            title=track.title,
            color=Color(randomizer.randint(0, 0xFFFFFF)),
        )
        embed.url = track.link

        if track.description is not None:
            embed.description = shorten(track.description, 75)

        if track.thumbnail_url is not None:
            embed.set_thumbnail(self.track.thumbnail_url)

        if track.uploader_name is not None:
            embed.set_author(
                name=track.uploader_name,
                url=track.uploader_url,
            )
        elif track.creator_name is not None:
            embed.set_author(name=track.creator_name)

        embed.set_footer(
            text=(
                "Live broadcast"
                if track.duration is None else
                f"Duration: {track.duration}"
                + convert_optional_string(
                    lambda x: " | Average rating: {rating_string}\n".format(
                        rating_string=int(x) * '\N{White Medium Star}',
                    ),
                    track.average_rating,
                )
            )
        )

        if (
            track.comment_count is not None
            or track.repost_count is not None
            or track.view_count is not None
            or track.like_count is not None
            or track.dislike_count is not None
        ):
            embed.add_field(
                name="Statistics",
                value=(
                    convert_optional_string(
                        lambda x: f"`Likes:` {x}\n",
                        track.like_count,
                    )
                    + convert_optional_string(
                        lambda x: f"`Dislikes:` {x}\n",
                        track.dislike_count,
                    )
                    + convert_optional_string(
                        lambda x: f"`Views:` {x}\n",
                        track.view_count,
                    )
                    + convert_optional_string(
                        lambda x: f"`Comments:` {x}\n",
                        track.comment_count,
                    )
                    + convert_optional_string(
                        lambda x: f"`Reposts:` {x}\n",
                        track.repost_count,
                    )
                ),
                inline=False
            )

        if (
            track.series_title is not None
            or track.alternative_title is not None
            or track.location is not None
            or track.disc_number is not None
        ):
            embed.add_field(
                name="Additional information",
                value=(
                    convert_optional_string(
                        lambda x: f"`Alternative title:` {x}\n",
                        track.alternative_title,
                    )
                    + convert_optional_string(
                        lambda x: f"`Location:` {x}\n",
                        track.location,
                    )
                    + convert_optional_string(
                        lambda x: f"`Series name:` {x}\n",
                        track.series_title,
                    )
                    + convert_optional_string(
                        lambda x: f"`Disk number:` {x}\n",
                        track.disc_number,
                    )
                ),
                inline=False
            )

        if (
            track.tags is not None
            or track.categories is not None
            or track.genres_string is not None
            or track.artists_string is not None
        ):
            embed.add_field(
                name="Classification",
                value=(
                    convert_optional_string(
                        lambda x: f"`Tags:` {', '.join(x)}\n",
                        track.tags,
                    )
                    + convert_optional_string(
                        lambda x: f"`Categories:` {', '.join(x)}\n",
                        track.categories,
                    )
                    + convert_optional_string(
                        lambda x: f"`Genres:` {x}\n",
                        track.genres_string,
                    )
                    + convert_optional_string(
                        lambda x: f"`Artists:` {x}\n",
                        track.artists_string,
                    )
                ),
                inline=False
            )

        if (
            track.release_at is not None
            or track.upload_at is not None
        ):
            embed.add_field(
                name="Release",
                value=(
                    convert_optional_string(
                        lambda x: f"`Release at:` {format_datetime(x)}\n",
                        track.release_at,
                    )
                    + convert_optional_string(
                        lambda x: f"`Upload at:` {format_datetime(x)}\n",
                        track.upload_at,
                    )
                ),
                inline=False
            )

        if track.track_title is not None:
            embed.add_field(
                name="Track Information",
                value=(
                    f"`Title:` {track.track_title}\n"
                    + convert_optional_string(
                        lambda x: f"`Id:` {x}\n",
                        track.track_id,
                    )
                    + convert_optional_string(
                        lambda x: f"`Number:` {x}\n",
                        track.track_number,
                    )
                ),
                inline=False
            )

        if track.channel_title is not None:
            embed.add_field(
                name="Channel Information",
                value=(
                    f"`Name:` {track.channel_title}\n"
                    + convert_optional_string(
                        lambda x: f"`Id:` {x}\n",
                        track.channel_id,
                    )
                    + convert_optional_string(
                        lambda x: f"`Url:` {x}\n",
                        track.channel_url,
                    )
                ),
                inline=False
            )

        if track.album_title is not None:
            embed.add_field(
                name="Album Information",
                value=(
                    f"`Name:` {track.album_title}\n"
                    + convert_optional_string(
                        lambda x: f"`Type:` {x}\n",
                        track.album_types_string,
                    )
                    + convert_optional_string(
                        lambda x: f"`Artists:` {x}\n",
                        track.album_artists_string,
                    )
                ),
                inline=False
            )

        if track.game_name is not None:
            embed.add_field(
                name="Game Information",
                value=(
                    f"`Name:` {track.game_name}\n"  # TODO?: Game title
                    + convert_optional_string(
                        lambda x: f"`Id:` {x}\n",
                        track.game_id,
                    )
                    + convert_optional_string(
                        lambda x: f"`Url:` {x}\n",
                        track.game_url,
                    )
                ),
                inline=False
            )

        if track.season_title is not None:
            embed.add_field(
                name="Season Information",
                value=(
                    f"`Name:` {track.season_title}\n"
                    + convert_optional_string(
                        lambda x: f"`Id:` {x}\n",
                        track.season_id,
                    )
                    + convert_optional_string(
                        lambda x: f"`Number:` {x}\n",
                        track.season_number,
                    )
                ),
                inline=False
            )

        if track.chapter_title is not None:
            embed.add_field(
                name="Chapter Information",
                value=(
                    f"`Name:` {track.chapter_title}\n"
                    + convert_optional_string(
                        lambda x: f"`Id:` {x}\n",
                        track.chapter_id,
                    )
                    + convert_optional_string(
                        lambda x: f"`Number:` {x}\n",
                        track.chapter_number,
                    )
                ),
                inline=False
            )

        if track.episode_title is not None:
            embed.add_field(
                name="Episode Information",
                value=(
                    f"`Name:` {track.episode_title}\n"
                    + convert_optional_string(
                        lambda x: f"`Id:` {x}\n",
                        track.episode_id,
                    )
                ),
                inline=False
            )

        return embed

