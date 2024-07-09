'use strict'

const MapObject = {}

MapObject.onEnterInner = function () {
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
    } else {
      const medal = this.def['SetWhenDone']['Medals'][0]
      const hasMedal = this.game.mulle.user.Car.hasMedal(medal)
      if (!hasMedal) {
        //TODO: Play sound
        this.game.mulle.user.Car.addMedal(medal)
      }
    }
  }
}

export default MapObject
