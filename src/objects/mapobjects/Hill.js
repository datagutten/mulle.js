'use strict'

const MapObject = {}

MapObject.onEnterInner = function (car) {
  console.log('enter hill, custom object', this)

  if (this.opt.HillType === '#SmallHill') {
    if (!this.game.mulle.user.Car.criteria.SmallHill) {
      //Small hill, engine too weak
      this.game.mulle.playAudio(this.def.Sounds[0])
    }
  } else {
    if (!this.game.mulle.user.Car.criteria.BigHill) {
      //Big hill, engine too weak
      this.game.mulle.playAudio(this.def.Sounds[1])
    }
  }
}

export default MapObject
