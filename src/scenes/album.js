/* global Phaser */
import MulleState from './base'

import TextInput from '../objects/TextInput'
import MulleSprite from '../objects/sprite'
import MulleBuildCar from '../objects/buildcar'
import MulleButton from '../objects/button'
import MulleFileBrowser from '../objects/MulleFileBrowser'
import LoadSaveCar from '../util/LoadSaveCar'
import DirectorHelper from '../objects/DirectorHelper'

/**
 * Album UI
 */
class AlbumState extends MulleState {
  /**
   * Create a sprite with director position
   * @param {string} dir Director movie
   * @param {string|int} num Director number or name
   * @returns {Phaser.Sprite}
   */
  positionSprite (dir, num) {
    const image = this.game.mulle.getDirectorImage(dir, num)
    const x = 320 - image.frame.regpoint.x
    const y = 240 - image.frame.regpoint.y
    return new Phaser.Sprite(this.game, x, y, image.key, image.name)
  }

  init (mode) {
    this.mode = mode
  }

  preload () {
    this.DirResource = '06.DXR'
    super.preload()
    this.game.load.pack('album', 'assets/album.json', null, this)
    this.game.load.pack('fileBrowser', 'assets/fileBrowser.json', null, this)
  }

  buildPages () {
    let pageNumSprite

    for (let page = 1; page <= 12; page++) {
      if (this.loadSave.isSaved(page)) { // Is a car saved on this page?
        pageNumSprite = this.positionSprite(this.DirResource, page + 60)
      } else {
        pageNumSprite = this.positionSprite(this.DirResource, page + 48)
      }

      if (page === this.selectedPage) {
        if (this.pagenumSpriteSelected) {
          this.pagenumSpriteSelected.destroy()
        }

        this.pagenumSpriteSelected = this.positionSprite(this.DirResource, page + 72)
        this.game.add.existing(this.pagenumSpriteSelected)
      } else {
        const button = MulleButton.fromRectangle(this.game, pageNumSprite.x, pageNumSprite.y, 40, 40, {
          click: () => {
            this.setPage(page)
          }
        })

        this.game.add.existing(button)
      }

      this.game.add.existing(pageNumSprite)
    }
  }

  /**
   * Select album page
   * @param page
   */
  setPage (page) {
    this.selectedPage = page
    this.game.mulle.playAudio('06e003v0')
    this.showSavedCar(page)
    this.buildPages()
  }

  /**
   * Show a car in the album
   */
  albumCar (parts = null) {
    if (this.albumCarImage) {
      this.albumCarImage.destroy()
    }

    this.albumCarImage = new MulleBuildCar(this.game, 320, 240, parts, true, false)
    this.background_layer.add(this.albumCarImage)
  }

  /**
   * Picture in the left corner ready for pasting
   */
  showPasteFrame () {
    this.imageFrame = new MulleButton(this.game, 67, 401, {
      imageDefault: [this.DirResource, 159],
      click: () => { this.pasteCar() }
    })

    this.game.add.existing(this.imageFrame)

    this.pasting_car = new MulleBuildCar(this.game, 0, 400, null, true, false)
    this.pasting_car.height = this.pasting_car.height / 2
    this.pasting_car.width = this.pasting_car.width / 2
    this.game.add.existing(this.pasting_car)
  }

  /**
   * Paste a car in the album
   */
  pasteCar () {
    this.imageFrame.destroy()
    this.imageFrame.displaySprite.visible = false
    this.pasting_car.destroy()
    this.albumCar()
    this.game.mulle.user.Car.Name = this.carName.value()

    this.loadSave.saveCurrentCar(this.selectedPage)
  }

  /**
   * Build the saved car
   * @param {int} page Album page
   */
  buildSavedCar (page) {
    let partId
    const [parts, medals, name] = this.loadSave.loadCar(page)
    // Place redundant parts in the junk yard
    for (partId of this.game.mulle.user.Car.Parts) {
      if (!(partId in parts)) {
        if (this.game.mulle.PartsDB[partId].master) { // Un-morph parts
          partId = this.game.mulle.PartsDB[partId].master
        }

        // Place the part in the junk yard
        this.game.mulle.user.addPart('Pile1', partId, null, true)
      }
    }

    this.removeParts(parts) // Remove the parts from wherever they are
    this.game.mulle.user.Car.Parts = []
    for (partId of parts) {
      this.game.mulle.user.Car.Parts.push(partId)
    }
    this.game.mulle.user.Car.Medals = medals
    this.game.mulle.user.Car.Name = name
    this.game.mulle.user.Car.updateStats()
    this.close()
  }

  /**
   * Show the saved car in the album
   * @param {int} page Album page
   */
  showSavedCar (page) {
    if (this.loadSave.isSaved(page)) {
      const [parts, medals, name] = this.loadSave.loadCar(page)
      this.albumCar(parts)
      this.parts = parts
      this.carName.text(name)
      this.showMedals(medals)
      if (this.mode === 'load') this.fetchButton.show()
    } else {
      if (this.albumCarImage) { this.albumCarImage.destroy() }
      if (this.mode === 'load') { this.fetchButton.hide() }
      if (this.medals) { this.medals.destroy(true) }
    }
  }

  /**
   * Remove a part from junk piles, shop floor and yard
   * @param {int} partId Part id
   */
  removePart (partId) {
    if (this.game.mulle.PartsDB[partId].master) { // Un-morph parts
      partId = this.game.mulle.PartsDB[partId].master
    }

    for (const pile in this.game.mulle.user.Junk) {
      if (partId in this.game.mulle.user.Junk[pile]) {
        console.log(`Remove part ${partId} from ${pile}`)
        delete this.game.mulle.user.Junk[pile][partId]
      }
    }
  }

  /**
   * Remove multiple parts from junk piles, shop floor and yard
   * @param {array} parts Array with part ids
   */
  removeParts (parts) {
    for (const part of parts) {
      this.removePart(part)
    }
  }

  importCar () {
    this.browser = new MulleFileBrowser(this.game, (data) => {
      this.loadSave.importCar(this.selectedPage, data)
      this.showSavedCar(this.selectedPage)
    })
    this.album_ui.add(this.browser)
  }

  showMedals (medals) {
    if (this.medals) { this.medals.destroy(true) }
    this.medals = this.game.add.group()
    let count = 1
    for (const medal of medals) {
      const { key, frame } = this.game.mulle.getDirectorImage(this.DirResource, 20 + medal)
      const sprite = new Phaser.Sprite(this.game, 550, 55 * count, key, frame.name)
      this.medals.add(sprite)
      count++
    }
  }

  create () {
    this.game.mulle.addAudio('album')
    super.create()
    this.loadSave = new LoadSaveCar(this.game)

    this.background_layer = this.game.add.group()
    this.album_ui = this.game.add.group()
    this.background = new MulleSprite(this.game, 320, 240)
    this.background.setDirectorMember(this.DirResource, 93)
    this.background_layer.add(this.background)

    // Car name
    this.name_input = DirectorHelper.sprite(this.game, 210, 427, this.DirResource, 101, false, false)
    this.album_ui.add(this.name_input)
    this.carName = new TextInput(this.game, this.name_input.x + 5, this.name_input.y + 5, 203, 20)
    this.carName.id('car_name')

    if (this.mode === 'save') {
      this.game.mulle.playAudio('06e002v0', () => {
        this.game.mulle.playAudio('06d001v0')
      })

      this.showPasteFrame()

      this.export_button = new MulleButton(this.game, 487, 413, {
        imageDefault: ['06.DXR', 164],
        click: () => {
          console.warn('Export car not implemented')
        }
      })

      this.game.add.existing(this.export_button)
    } else { // Show picture
      this.game.mulle.playAudio('07d001v0')

      this.fetchButton = new MulleButton(this.game, 76, 400, {
        imageDefault: [this.DirResource, 162],
        click: () => {
          this.buildSavedCar(this.selectedPage)
        }
      })

      this.album_ui.add(this.fetchButton)
      this.carName.input.readOnly = true

      this.importButton = new MulleButton(this.game, 487, 413, {
        imageDefault: ['06.DXR', 161],
        click: () => {
          this.importCar()
        }
      })
      this.album_ui.add(this.importButton)
    }

    this.close_button = new MulleButton(this.game, 554, 414, {
      imageDefault: ['06.DXR', 153],
      click: () => {
        console.log('Close album')
        this.close()
      }
    })

    this.album_ui.add(this.close_button)
    this.setPage(1)
  }

  close () {
    this.game.state.start('garage')
  }

  shutdown (game) {
    this.cutscene = 83
    this.carName.remove()
    super.shutdown(game)
  }
}

export default AlbumState
