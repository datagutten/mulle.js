import MulleState from './base'

import MulleSprite from '../objects/sprite'
import MulleBuildCar from '../objects/buildcar'
import MulleActor from '../objects/actor'
import blinkThing from '../util/blinkThing'
import SubtitleLoader from '../objects/SubtitleLoader'

class ViolaState extends MulleState {
  preload () {
    super.preload()
    this.game.load.pack('viola', 'assets/viola.json', null, this)
    this.subtitles = new SubtitleLoader(this.game, 'viola', ['english'])
    this.subtitles.preload()
  }

  create () {
    super.create()
    
    this.game.mulle.addAudio('viola')
    this.subtitles.load()

    // Play background sound
    this.game.mulle.playAudio('89e001v0')

    // Background
    var background = new MulleSprite(this.game, 320, 240)
    background.setDirectorMember('89.DXR', 1)
    this.game.add.existing(background)

    // The car (without Salka/Mulle)
    this.car = new MulleBuildCar(this.game, 445, 370, null, false, false)
    this.game.add.existing(this.car)

    // Buffa with animation
    var buffa = new MulleActor(this.game, 360, 320, 'buffa')
    buffa.setDirectorMember('00.CXT', 214)
    this.game.add.existing(buffa)
    this.game.mulle.actors.buffa = buffa
    
    let animationCount = 0
    let isWaiting = false
    let buffaTimer = this.game.time.events.loop(150, () => {
        if (!isWaiting && animationCount < 8) {
            buffa.animations.play('scratch1', null, false)
            buffa.animations.currentAnim.onComplete.addOnce(() => {
                buffa.setDirectorMember('00.CXT', 214)
                animationCount++
                
                if (animationCount >= 8) {
                    isWaiting = true
                    this.game.time.events.add(3000, () => {
                        animationCount = 0
                        isWaiting = false
                    })
                }
            })
        }
    })

    // Viola in the window
    var viola = new MulleSprite(this.game, 246, 154)
    viola.setDirectorMember('89.DXR', 18)
    this.game.add.existing(viola)

    // Window animation
    let frame = 18
    let animationTimer = this.game.time.events.loop(300, () => {
        frame++
        if (frame > 20) {
            frame = 18
        }
        viola.setDirectorMember('89.DXR', frame)
    })

    // Show the tank directly with correct properties
    var tank = new MulleSprite(this.game, 2, 332)
    tank.setDirectorMember('CDDATA.CXT', 436)
    tank.partId = 172
    tank.properties = {
        Weight: 4,
        Color: 1,
        Funnyfactor: 5
    }
    tank.requires = ['#b1']
    tank.covers = ['#a5', '#a6', '#a7', '#b1']
    this.game.add.existing(tank)

    // Play the dialogs one after another
    this.game.mulle.playAudio('89d001v0', () => {
        this.game.mulle.playAudio('89d003v0', () => {
                this.game.mulle.user.Junk.yard[172] = { 
                    x: this.game.rnd.integerInRange(290, 580),
                    y: 440
                }

                this.game.time.events.remove(buffaTimer)
                buffa.animations.stop()
                
                // Use blinkThing for the disappearing effect
                new blinkThing(this.game, tank, () => {
                    this.game.mulle.stopAudio('89e001v0')
                    this.game.time.events.remove(animationTimer)
                    this.game.time.events.remove(buffaTimer)
                    buffa.animations.stop()
                    this.game.state.start('world')
                }, this)
            })
        })
  }

  shutdown() {
    this.game.mulle.stopAudio('viola')
    super.shutdown()
  }
}

export default ViolaState 