from enum import Enum
import re
from selenium import webdriver

import time

# Instantiate an instance of Remote WebDriver with the desired capabilities.
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.command import Command
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Rarity(Enum):
    normal = 1
    elite = 2
    elite_2 = 3
    elite_3 = 4
    heroic = 5
    colossus = 6
    titan = 7


class Npc:
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y

class Enemy(Npc):

    def __init__(self, name: str, x: int, y: int, lvl: int, rarity: Rarity, in_group: bool):
        super().__init__(name, x, y)
        self.lvl = lvl
        self.rarity = rarity
        self.in_group = in_group


class Door(Npc):
    def __init__(self, name: str, x: int, y: int, walkable: bool):
        super().__init__(name, x, y)
        self.walkable = walkable


class MargoHandler:

    def __init__(self) -> None:
        super().__init__()
        self.driver = webdriver.Chrome()

        self.width = None
        self.height = None
        self.npcs = []
        self.doors = []
        self.enemies = []

    def game_start(self):

        self.driver.get("https://www.margonem.pl/")
        time.sleep(2)
        self.login("margoai", "***")
        time.sleep(1)
        self.driver.find_element_by_class_name('enter-game').click()
        time.sleep(0.5)

    def login(self, username: str, password: str) -> bool:
        login_button = self.driver.find_element_by_class_name("button-login")

        if login_button is None: return False

        # We are at the login page, lets login
        login_button.click()

        time.sleep(1)

        self.driver.find_element_by_name("login").send_keys(username)
        time.sleep(0.5)
        self.driver.find_element_by_name("password").send_keys(password, Keys.ENTER)
        time.sleep(0.5)

        return True

    def get_map_size(self):
        ground_widget = self.driver.find_element_by_id("ground")
        pixel_width: str = ground_widget.value_of_css_property("width")
        pixel_height: str = ground_widget.value_of_css_property("height")
        if pixel_height and pixel_width:
            self.width = int(pixel_width[:-2]) // 32
            self.height = int(pixel_height[:-2]) // 32
            print(f"Map size ({self.width},{self.height})")
        else:
            print("Could not load map size")
            self.width = None
            self.height = None

    def switch_to_old_interface(self):
        self.driver.find_element_by_class_name('widget-config').click()
        time.sleep(0.5)
        self.driver.find_element_by_class_name('change-interface-btn').click()
        time.sleep(1)

    def walk(self, direction, duration):
        webdriver.ActionChains(self.driver).key_down(direction).perform()
        time.sleep(duration)
        webdriver.ActionChains(self.driver).key_up(direction).perform()

    @staticmethod
    def get_coordinates(widget):
        pixel_width: str = widget.value_of_css_property("left")
        pixel_height: str = widget.value_of_css_property("top")
        if pixel_height and pixel_width:
            width = int(pixel_width[:-2]) // 32
            height = int(pixel_height[:-2]) // 32
            return width,height
        else:
            print("Could not load widget coordinates")
            return None,None

    def is_door(self, div_id):
        if div_id is None: return False

        widget = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, div_id)))
        if widget is None:
            return False

        image_url: str = widget.value_of_css_property("background-image")
        match = re.search(r"exit", image_url)
        return match is not None

    def get_all_npc(self):
        npcs = self.driver.find_elements_by_class_name("npc")

        if npcs is None or len(npcs) == 0:
            print("No npcs found")
            return

        for npc_div in npcs:

            tip = npc_div.get_attribute("tip")

            if tip is None:
                continue

            name = re.search(r"<b>(.+?)</b>", tip).group(1)
            coords = self.get_coordinates(npc_div)

            lvl = re.search(r"<span >(.+?) lvl<\/span>", tip)

            # Enemy found, add to list
            if lvl is not None:
                lvl = int(lvl.group(1))
                self.enemies.append(Enemy(name, coords[0], coords[1], lvl, Rarity.normal, False))
            # Found npc is door
            elif self.is_door(npc_div.get_property("id")):
                self.doors.append(Door(name, coords[0], coords[1], True))
            # Found npc
            else:
                self.npcs.append(Npc(name, coords[0], coords[1]))

        print("NPCs loaded")
        print(f"Enemies: {len(self.enemies)}")
        print(f"NPCs: {len(self.npcs)}")
        print(f"Doors: {len(self.doors)}")
