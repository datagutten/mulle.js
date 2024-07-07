'use strict'

/**
 *
 * @type {{MapObject}}
 * Map 7, 15, 23
 */
const MapObject = {}

MapObject.onCreate = function () {
  this.animationHelper.add('idle', 'normal', 1, 12, true)

  const parting = this.animationHelper.add('parting', 'Parting', 1, 5)
  parting.onComplete.add(() => {
    this.animations.play('parted')
  })

  this.animationHelper.add('parted', 'Outer', 1, 12, true)

  const gathering = this.animationHelper.add('gathering', 'Gathering')
  gathering.onComplete.add(() => {
    this.animations.play('idle')
  })

  this.animations.play('idle')
}

MapObject.onEnterInner = function (car) {
  const allowed = this.game.mulle.user.Car.getProperty('horntype', 0) >= 1

  const horns = ['05e050v0', '05e049v0', '05e044v0', '05e042v0', '05d013v0']

  if (allowed) {
    this.animations.play('parting')

    if (!this.playedSound) {
      this.game.mulle.playAudio(horns[this.game.mulle.user.Car.getProperty('horntype', 0) - 1])

      this.playedSound = true

      const sound = this.game.mulle.playAudio(this.def.Sounds[1])
      sound.onStop.addOnce(() => {
        this.playedSound = null
      })
    }
  } else {
    if (!this.playedSound) {
      this.playedSound = true

      const error_sound = this.game.mulle.playAudio(this.def.Sounds[0])
      error_sound.onStop.addOnce(() => {
        this.playedSound = null
      })
    }

    car.speed = 0
    car.stepback(2)
    this.enteredInner = false
  }
}

MapObject.onExitInner = function () {
  this.animations.play('gathering')

}

MapObject.onExitOuter = function () {
  this.game.mulle.stopAudio(this.def.Sounds[1]);
}

export default MapObject
