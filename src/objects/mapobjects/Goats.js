'use strict'

import ObjectAnimation from './animation'

/**
 *
 * @type {{MapObject}}
 * Map 5
 */
const MapObject = {}

MapObject.onCreate = function () {
  const animations = new ObjectAnimation(this, 'CDDATA.CXT')

  animations.add('idle', 'normal', 1, 4, true)

  const parting = animations.add('parting', 'Parting')
  parting.onComplete.add(() => {
    this.animations.play('parted')
  })

  animations.add('parted', 'Outer', 1, 4, true)

  const gathering = animations.add('gathering', 'Gathering')
  gathering.onComplete.add(() => {
    this.animations.play('idle')
  })

  this.animations.play('idle')
}

MapObject.onEnterInner = function (car) {
  const allowed = this.game.mulle.user.Car.getProperty('horntype', 0) >= 5

  const horns = ['05e050v0', '05e049v0', '05e044v0', '05e042v0', '05d013v0']

  if (allowed) {
    this.animations.play('parting')

    if (!this.playedSound) {
      this.game.mulle.playAudio(horns[this.game.mulle.user.Car.getProperty('horntype', 0) - 1])

      this.playedSound = true

      const sound = this.game.mulle.playAudio(this.def.Sounds[1]) // Goat sounds
      sound.onStop.addOnce(() => {
        this.playedSound = null
      })
    }
  } else {
    if (!this.playedSound) {
      this.playedSound = true

      const sound = this.game.mulle.playAudio(this.def.Sounds[0])
      sound.onStop.addOnce(() => {
        this.playedSound = null
      })
    }

    car.speed = 0
    car.stepback(2)
    this.enteredInner = false
  }
}

MapObject.onExitInner = function (car) {
  this.animations.play('gathering')

}

MapObject.onExitOuter = function (car) {
  this.game.mulle.stopAudio(this.def.Sounds[1]);
}

export default MapObject
