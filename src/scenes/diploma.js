import MulleState from './base'
import DirectorHelper from '../objects/DirectorHelper'
import MulleBuildCar from '../objects/buildcar'

class DiplomaState extends MulleState {
  init(previous) {
    this.previousState = previous
  }

  preload () {
    this.DirResource = '08.DXR'
    super.preload()
    this.game.load.pack('diploma', 'assets/diploma.json', null, this)
    this.load.json('strings', 'assets/diploma-strings.json')
  }

  create () {
    console.log('Previous state', this.previousState)
    this.scroll_level = 0
    this.whiteLayer = this.add.group()
    this.background_layer = this.game.add.group()
    this.ui_layer = this.game.add.group()
    this.scroll_layer = this.game.add.group()

    this.header = DirectorHelper.sprite(this.game, 14,2, this.DirResource, 71, false, false)

    this.scroll_layer.add(this.header)

    this.rightMenuRectangle = new Phaser.Rectangle(0, -9, 587, 503)

    this.wood = DirectorHelper.sprite(this.game, 614, 240, this.DirResource, 15)
    this.ui_layer.add(this.wood)

    this.upButton = DirectorHelper.button(this.game, 612, 20, this.scrollUp, this, this.DirResource, 17, 17, true)
    this.ui_layer.add(this.upButton)

    this.downButton = DirectorHelper.button(this.game, 612, 186, this.scrollDown, this, this.DirResource, 18, 18, true)
    this.ui_layer.add(this.downButton)

    this.printButton = DirectorHelper.button(this.game, 612, 378, () => {console.log('print')}, this, this.DirResource, 67,67, true)
    this.ui_layer.addChild(this.printButton)

    this.closeButton = DirectorHelper.button(this.game, 611, 441, this.close, this, this.DirResource, 68, 68, true)
    this.ui_layer.add(this.closeButton)

    const graphics = this.add.graphics(0, 0, this.whiteLayer);
    graphics.beginFill(0xFFFFFF)
    graphics.drawRect(572, 0, 13, 479)

    graphics.drawRect(52, 100, 518, 368) //ToBeCaptured

    graphics.drawRect(0, 0, 587, 503)

    const strings = this.game.cache.getJSON('strings')

    this.userName = new Phaser.Text(this.game, 0, 0, this.game.mulle.user.UserId, {
      font: '36pt Arial',
      boundsAlignH: 'center',
      boundsAlignV: 'center'
    })
    this.userName.setTextBounds(150, this.header.height + this.header.y - 6, 303, 43)
    this.scroll_layer.add(this.userName)

    this.forCarText = new Phaser.Text(this.game,  0, 0, strings[this.DirResource][69], {
      font: '24pt Arial',
      boundsAlignH: 'center',
      boundsAlignV: 'center'
    })
    this.forCarText.setTextBounds(150, this.header.height + this.header.y + 36, 303, 29)
    this.scroll_layer.addChild(this.forCarText)

    this.carName = new Phaser.Text(this.game, 0, 0, this.game.mulle.user.Car.Name, {
      font: '36pt Arial',
      boundsAlignH: 'center',
      boundsAlignV: 'center'
    })
    this.carName.setTextBounds(150, this.header.height + this.header.y + 56, 303, 44)
    this.scroll_layer.add(this.carName)

    this.carImageRectangle = new Phaser.Rectangle(52,this.header.height + this.header.y + 100, 518, 368)
    this.carImage = new MulleBuildCar(this.game, this.carImageRectangle.centerX, this.carImageRectangle.centerY, null, true)
    this.scroll_layer.add(this.carImage)

    this.medals = this.game.add.group(this.scroll_layer)

    let count = 1
    let medal_x = 32

    for (const medal of this.game.mulle.user.Car.Medals) {
      const { key, frame } = this.game.mulle.getDirectorImage(this.DirResource, 20 + medal)
      const medalSprite = new Phaser.Sprite(this.game, medal_x, 623, key, frame.name)
      this.medals.add(medalSprite)
      medalSprite.width = 60
      medalSprite.height = 60
      medal_x = medalSprite.right + 40

      const medalName = new Phaser.Text(this.game, 0, 0, strings[this.DirResource][80 + medal], {
        font: '11pt Times New Roman',
        boundsAlignH: 'center',
        boundsAlignV: 'center',
        wordWrap: true,
        wordWrapWidth: medalSprite.width
      })
      console.log(medalSprite)
      medalName.setTextBounds(medalSprite.x, medalSprite.bottom + 10, medalSprite.width, 40)
      this.medals.add(medalName)

      count++
    }

    const frame = this.add.graphics(0, 0, this.scroll_layer);
    frame.beginFill(0x000000)
    const border = frame.drawRect(12, 2, 2, 777) //Left border
    frame.drawRect(572, 2, 2, 777) // Right border

    // Line is 39 pixels from top of image, subtract to make bottom of side borders match bottom border
    //Texture 08b004v0
    this.bottom = DirectorHelper.sprite(this.game, 14, border.bottom - 39, this.DirResource, 70, false, false)
    this.scroll_layer.add(this.bottom)
  }


  scrollUp() {
    if(this.scroll_level > 0) {
      this.scroll_layer.forEach((child) => {
        child.y = child.y + 200
      })
      this.scroll_level--
    }
  }

  scrollDown() {
    if(this.scroll_level < 2) {
      this.scroll_layer.forEach((child) => {
        child.y = child.y - 200
      })
      this.scroll_level++
    }
  }

  close () {
    this.game.state.start(this.previousState)
  }
}

export default DiplomaState