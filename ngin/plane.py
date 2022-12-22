#!/usr/bin/env python3
from ngin.ngin import Head, CStageInfo, JoystickDirectionals, ActionEvent, CmdInfo, CObject, CVisible, CPhysical, CAction, CActionType, BodyShape, BodyType, Cmd
import json
import math
from ngin.ngin import Nx, EventHandler, CObjectInfo

class MyHandler(EventHandler):
  def __init__(self, nx):
    self.nx = nx      
    self.key_down_left = False
    self.key_down_right = False
    self.actor_contacts = set()
    self.actor_jump_count = 0
    self.dynamic_id = 1000
    self.facingLeft = False  
    self.ready = False          

  def go_right(self):
    self.nx.angular(100, 1)

  def go_left(self):
    self.nx.angular(100, -1)

  def stop(self):
    self.nx.angular(100, 0)

  def get_dynamic_id(self):
    self.dynamic_id += 1
    return self.dynamic_id

  def missile(self):
    info = self.nx.get_obj_info(100)
    info = CObjectInfo(info.floats)
    new_id = self.get_dynamic_id()
    o = self.nx.obj_builder(new_id, "missile")

    p = self.nx.physical_builder(o, BodyShape.rectangle, info.x-0.5 + 2*math.sin(info.angle), info.y-0.5 - 2*math.cos(info.angle))
    p.angle = info.angle
    v = self.nx.visible_builder(o, [nx.action_builder('kenney_pixelshmup/tiles_packed.png', 16, [1, 2, 3])])
    self.nx.send(Head.cobject, o, True)
    self.nx.forward(new_id, 0, 20)
    self.nx.timer(new_id, 0.7)

  def key_handler(self, c):
    c = c.key
    if c.isPressed == False:
      match c.name:
        case 'Arrow Left':
          self.key_down_left = False
          if self.key_down_right:
            self.go_right()
          else:
            self.stop()	
        case 'Arrow Right':
          self.key_down_right = False
          if self.key_down_left:
            self.go_left()
          else:
            self.stop()
    else:
      match c.name:
        case 'Arrow Left':
          self.key_down_left = True         
          self.go_left()
        case 'Arrow Right':
          self.key_down_right = True            
          self.go_right()
        case 'Arrow Up':	
          self.missile()

  def contact_handler(self, c):
    contact = c.contact
    if contact.isEnded == False:
      if contact.info2 == 'missile':
        self.nx.remove(contact.id2)

        o = self.nx.obj_builder(self.get_dynamic_id(), "fire")
        o.tid = contact.id1
        self.nx.visible_builder(o, [nx.action_builder('kenney_pixelshmup/tiles_packed.png', 16, [5])])
        self.nx.send(Head.cobject, o, True)

  def event_handler(self, c):
    event = c.event
    if event.info == 'missile':
      self.nx.remove(event.id)

def demo():
  nx = Nx('bonsoirdemo', 4040)
  nx.set_event_handler(MyHandler(nx))
  f = open('./data/planes0.tmj', "r")
  j = json.loads(f.read())
  f.close()
  t = j['layers'][0]
  tileSize = j['tilewidth']
  nx.send(Head.stage, nx.stage_builder(t['width'], t['height']), True)  

  nx.send(Head.cobject, nx.tiles_builder('kenney_pixelshmup/tiles_packed.png', tileSize, t['width'], t['height'], t['data']))

  o = nx.obj_builder(100, "hero")
  p = nx.physical_builder(o, BodyShape.circle, 11, 11)
  p.angle = 1.5
  p.width = 2
  p.height = 2
  v = nx.visible_builder(o, [nx.action_builder('kenney_pixelshmup/ships_packed.png', 32, [1])])
  v.width = 2
  v.height = 2
  nx.send(Head.cobject, o, True)

  nx.follow(100)
  nx.forward(100, 0, 5)

  o = nx.obj_builder(200, "enemy")
  p = nx.physical_builder(o, BodyShape.circle, 11, 0)
  p.width = 2
  p.height = 2
  v = nx.visible_builder(o, [nx.action_builder('kenney_pixelshmup/ships_packed.png', 32, [10])])
  v.width = 2
  v.height = 2
  nx.send(Head.cobject, o, True)

  nx.forward(200, 0, 5)
  nx.angular(200, 1)

  nx.main_loop()