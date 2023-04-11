# game_cover.py
#
# Copyright 2022-2023 kramo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import GdkPixbuf, GLib

from .save_cover import resize_animation


class GameCover:
    pixbuf = None
    path = None
    animation = None

    placeholder_pixbuf = GdkPixbuf.Pixbuf.new_from_resource_at_scale(
        "/hu/kramo/Cartridges/library_placeholder.svg", 400, 600, False
    )

    def __init__(self, picture, pixbuf=None, path=None):
        self.picture = picture
        self.new_pixbuf(pixbuf, path)

    def new_pixbuf(self, pixbuf=None, path=None):
        self.animation = None
        self.pixbuf = None
        self.path = None

        if pixbuf:
            self.pixbuf = pixbuf

        if path:
            if str(path).rsplit(".", maxsplit=1)[-1] == "gif":
                self.path = resize_animation(path)
                self.animation = GdkPixbuf.PixbufAnimation.new_from_file(str(self.path))
                self.anim_iter = self.animation.get_iter()
                self.update_animation(self.animation)
            else:
                self.path = path
                self.pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    str(path), 200, 300, False
                )

        if not self.pixbuf:
            self.pixbuf = self.placeholder_pixbuf

        if not self.animation:
            self.set_pixbuf(self.pixbuf)

    def get_pixbuf(self):
        return self.animation.get_static_image() if self.animation else self.pixbuf

    def get_animation(self):
        return self.path if self.animation else None

    def set_pixbuf(self, pixbuf):
        self.picture.set_pixbuf(pixbuf)

    def update_animation(self, animation):
        if self.animation == animation:
            self.anim_iter.advance()

            self.set_pixbuf(self.anim_iter.get_pixbuf())

            delay_time = self.anim_iter.get_delay_time()
            GLib.timeout_add(
                20 if delay_time < 20 else delay_time,
                self.update_animation,
                animation,
            )