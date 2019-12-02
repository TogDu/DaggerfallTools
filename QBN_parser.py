import struct 
import sys, os

TVH_MAP = {
	0x000000F3:"a1",
	0x000000F4:"a2",
	0x000000F5:"a3",
	0x000000F6:"a4",
	0x000000F7:"a5",
	0x000000F8:"a6",
	0x0000012A:"db",
	0x00000141:"mg",
	0x0000014B:"no",
	0x0000014F:"tg",
	0x000002CA:"eel",
	0x000002CF:"ice",
	0x000002D3:"gem",
	0x000002DD:"bow",
	0x000002E4:"man",
	0x000002E6:"map",
	0x000002E8:"len",
	0x000002EE:"inn",
	0x000002EE:"imp",
	0x000002EE:"off",
	0x000002EF:"key",
	0x000002F4:"mob",
	0x000002FB:"npc",
	0x000002FE:"rat",
	0x00000303:"orc",
	0x00000321:"yes",
	0x00000325:"spy",
	0x000005c7:"day1",
	0x000005c8:"day2",
	0x000005D7:"gem1",
	0x000005D8:"bear",
	0x000005D8:"gem2",
	0x000005D9:"gem3",
	0x000005DA:"gem4",
	0x000005DB:"bank",
	0x000005DC:"bard",
	0x000005EF:"bats",
	0x00000609:"ally",
	0x00000615:"book",
	0x00000617:"mace",
	0x00000619:"gems",
	0x0000061D:"fire",
	0x0000061F:"mage",
	0x00000625:"boss",
	0x00000625:"lady",
	0x00000627:"npc1",
	0x00000628:"npc2",
	0x00000629:"npc3",
	0x0000062A:"duel",
	0x0000062A:"foil",
	0x00000630:"gold",
	0x00000632:"lich",
	0x00000637:"orc1",
	0x00000638:"orc2",
	0x00000639:"orc3",
	0x0000063A:"orc4",
	0x0000063B:"home",
	0x0000063D:"necs",
	0x0000064F:"item",
	0x0000064F:"sage",
	0x0000065C:"iron",
	0x00000660:"pawn",
	0x00000664:"lord",
	0x0000066B:"monk",
	0x0000066D:"love",
	0x0000066F:"rats",
	0x00000673:"yes1",
	0x00000674:"yes2",
	0x00000675:"yes3",
	0x00000676:"yes4",
	0x00000677:"ring",
	0x00000677:"nono",
	0x00000677:"yes5",
	0x00000678:"yes6",
	0x00000679:"orcs",
	0x00000679:"note",
	0x0000067D:"rock",
	0x0000067E:"vamp",
	0x00000683:"time",
	0x00000686:"shop",
	0x00000691:"thug",
	0x0000069C:"star",
	0x000006B2:"wolf",
	0x00000957:"2dung",
	0x00000C2C:"agent",
	0x00000C48:"darkb",
	0x00000C4B:"decoy",
	0x00000C50:"child",
	0x00000C53:"delay",
	0x00000C6F:"mage1",
	0x00000C70:"mage2",
	0x00000C71:"arena",
	0x00000C71:"mage3",
	0x00000C72:"mage4",
	0x00000C7C:"elder",
	0x00000C7D:"bribe",
	0x00000C8C:"giant",
	0x00000C91:"gold1",
	0x00000C92:"gold2",
	0x00000CA2:"flesh",
	0x00000CA6:"heist",
	0x00000CA7:"enemy",
	0x00000CA9:"harpy",
	0x00000CA9:"magic",
	0x00000CAB:"gimme",
	0x00000CAF:"lamia",
	0x00000CB1:"mages",
	0x00000CC0:"maker",
	0x00000CC6:"ghost",
	0x00000CCC:"giver",
	0x00000CCF:"item1",
	0x00000CD0:"item2",
	0x00000CD1:"item3",
	0x00000CE4:"guard",
	0x00000CE5:"drugs",
	0x00000CEF:"dummy",
	0x00000CF2:"local",
	0x00000CF6:"metal",
	0x00000CF8:"crypt",
	0x00000CFC:"pearl",
	0x00000D06:"frost",
	0x00000D06:"rebel",
	0x00000D0F:"place",
	0x00000D17:"house",
	0x00000D1D:"noble",
	0x00000D1F:"mitem",
	0x00000D2D:"vamp1",
	0x00000D2E:"vamp2",
	0x00000D2F:"vamp3",
	0x00000D37:"patsy",
	0x00000D37:"time1",
	0x00000D38:"time2",
	0x00000D39:"time3",
	0x00000D3E:"nomap",
	0x00000D43:"money",
	0x00000D4C:"lover",
	0x00000D54:"thief",
	0x00000D60:"tiger",
	0x00000D6C:"other",
	0x00000D6F:"vamps",
	0x00000D78:"timer",
	0x00000D7F:"mummy",
	0x00000D83:"rogue",
	0x00000D84:"queen",
	0x00000D8F:"posse",
	0x00000D93:"qtime",
	0x00000D9C:"token",
	0x00000D9D:"widow",
	0x00000DA4:"nymph",
	0x00000DB4:"ruler",
	0x00000DB6:"total",
	0x00000DB6:"witch",
	0x00000DD5:"store",
	0x0000126C:"2agent",
	0x00001864:"badpcn",
	0x0000188D:"daedra",
	0x000018A8:"banker",
	0x000018D0:"dbgold",
	0x000018F4:"gaffer",
	0x000018FA:"damsel",
	0x00001915:"castle",
	0x00001934:"archer",
	0x00001944:"healer",
	0x00001945:"cleric",
	0x0000194C:"father",
	0x00001986:"amulet",
	0x00001998:"finger",
	0x000019B1:"escape",
	0x000019C1:"given1",
	0x000019D2:"dreugh",
	0x000019DA:"hermit",
	0x000019F9:"guard1",
	0x000019FA:"guard2",
	0x000019FB:"guard3",
	0x000019FC:"guard4",
	0x00001A04:"cousin",
	0x00001A1F:"palace",
	0x00001A3B:"guards",
	0x00001A40:"mggold",
	0x00001A50:"hooker",
	0x00001A54:"master",
	0x00001A5F:"house1",
	0x00001A60:"house2",
	0x00001A61:"house3",
	0x00001A68:"knight",
	0x00001A70:"lesser",
	0x00001A7C:"letter",
	0x00001A84:"scarab",
	0x00001A98:"ranger",
	0x00001AB3:"oneday",
	0x00001ACC:"hunter",
	0x00001ACC:"shaman",
	0x00001AD6:"school",
	0x00001AE8:"mondun",
	0x00001AE8:"qgiven",
	0x00001AEC:"qgiver",
	0x00001AF8:"shield",
	0x00001AFA:"target",
	0x00001B14:"reward",
	0x00001B26:"tavern",
	0x00001B35:"temple",
	0x00001B44:"weapon",
	0x00001B4B:"prince",
	0x00001B4C:"murder",
	0x00001B50:"poison",
	0x00001B56:"priest",
	0x00001B74:"spider",
	0x00001B77:"victim",
	0x00001B80:"potion",
	0x00001B86:"snitch",
	0x00001B94:"sister",
	0x00001BB3:"questg",
	0x00001BEE:"yesmap",
	0x00001BF7:"spouse",
	0x00001BFC:"wraith",
	0x00001C0C:"wizard",
	0x00001C57:"zombie",
	0x00002520:"2dagger",
	0x0000269F:"2palace",
	0x000026FC:"2letter",
	0x00002757:"2ransom",
	0x0000314B:"daedra1",
	0x0000314C:"daedra2",
	0x0000314D:"daedra3",
	0x0000314E:"daedra4",
	0x0000318D:"daedras",
	0x000031F6:"acrobat",
	0x00003205:"agentuk",
	0x00003221:"acolyte",
	0x00003238:"dbguild",
	0x00003254:"casfort",
	0x00003276:"chemist",
	0x000032AD:"failure",
	0x000032C0:"centaur",
	0x00003300:"breaker",
	0x00003346:"coastal",
	0x0000335C:"fighter",
	0x000033A2:"hideout",
	0x000033AD:"clothes",
	0x000033DE:"contact",
	0x00003407:"bowdung",
	0x00003429:"friend1",
	0x0000342A:"friend2",
	0x0000342B:"friend3",
	0x0000342C:"brother",
	0x0000342C:"friend4",
	0x0000344E:"duelist",
	0x0000345C:"burglar",
	0x0000345F:"package",
	0x00003493:"flowers",
	0x00003497:"mapdung",
	0x00003498:"dungeon",
	0x000034B8:"paladin",
	0x000034C5:"jewelry",
	0x000034C8:"mansion",
	0x000034D3:"marknpc",
	0x000034EF:"foundme",
	0x00003500:"killmon",
	0x00003527:"keydung",
	0x00003529:"letter1",
	0x0000352A:"letter2",
	0x00003536:"readmap",
	0x0000353C:"mfriend",
	0x0000355F:"message",
	0x00003573:"keytime",
	0x00003594:"mmaster",
	0x00003599:"grizzly",
	0x000035A4:"teacher",
	0x000035C7:"newdung",
	0x000035C7:"qgenemy",
	0x000035DA:"mondead",
	0x000035F4:"huntend",
	0x000035FC:"scholar",
	0x00003610:"seducer",
	0x00003628:"onehour",
	0x0000362F:"relitem",
	0x0000362F:"replace",
	0x00003637:"mondung",
	0x00003659:"reward1",
	0x0000365A:"reward2",
	0x0000365B:"reward3",
	0x00003670:"lovgold",
	0x00003679:"peryite",
	0x00003693:"revenge",
	0x000036A4:"monster",
	0x000036C0:"sneaker",
	0x000036DD:"vampire",
	0x000036FB:"weapons",
	0x0000375B:"spiders",
	0x00003760:"soldier",
	0x00003777:"myndung",
	0x00003784:"warrior",
	0x0000378E:"prophet",
	0x00003795:"success",
	0x00003798:"ukcrypt",
	0x000037B8:"traitor",
	0x000037E4:"queston",
	0x000037ee:"wayrest",
	0x0000383C:"upfront",
	0x0000387D:"witness",
	0x00005077:"2myndung",
	0x000063BC:"daedroth",
	0x000064E0:"champion",
	0x00006523:"fakename",
	0x0000659C:"daughter",
	0x000065A4:"castfort",
	0x0000672A:"gianteel",
	0x000067C7:"clothing",
	0x000067ED:"contact1",
	0x000067EE:"contact2",
	0x000067FE:"artifact",
	0x00006817:"conhouse",
	0x00006854:"assassin",
	0x0000688E:"dirtypit",
	0x000068D2:"atronach",
	0x00006936:"firsthit",
	0x00006944:"goldgoth",
	0x00006961:"dungeon1",
	0x00006962:"dungeon2",
	0x00006963:"dungeon3",
	0x00006977:"hintdung",
	0x000069A4:"hitguard",
	0x000069F4:"guardian",
	0x00006A05:"evilfocs",
	0x00006A19:"keptgems",
	0x00006A2F:"evilitem",
	0x00006A30:"informer",
	0x00006A44:"merchant",
	0x00006A7B:"dummyorc",
	0x00006AB0:"oblivion",
	0x00006AC7:"painting",
	0x00006B00:"lessgold",
	0x00006B19:"readnote",
	0x00006B27:"itemdung",
	0x00006B5E:"placemap",
	0x00006BCC:"nobleman",
	0x00006C2F:"newplace",
	0x00006C3C:"qgfriend",
	0x00006CA0:"mondung2",
	0x00006cda:"llugwych",
	0x00006CCC:"talisman",
	0x00006CF6:"huntstop",
	0x00006D79:"monster1",
	0x00006D7A:"monster2",
	0x00006D7B:"monster3",
	0x00006D7C:"monster4",
	0x00006D8F:"thankyou",
	0x00006DA7:"ringdung",
	0x00006DB0:"scorpion",
	0x00006DE4:"skeleton",
	0x00006DE7:"nononono",
	0x00006E13:"vampname",
	0x00006E2D:"vampires",
	0x00006E2F:"vampitem",
	0x00006E38:"mtraitor",
	0x00006E69:"weaponss",
	0x00006E71:"timeforq",
	0x00006F24:"qmonster",
	0x00006F50:"wereboar",
	0x00006F5B:"orsinium",
	0x00006F60:"villager",
	0x00006df6:"sentinel",
	0x00006FE5:"treasure",
	0x00006FF0:"sorceror",
	0x00006FF4:"smuggler",
	0x00006FF9:"queston1",
	0x00006FFA:"queston2",
	0x00007002:"werewolf",
	0x00007054:"spriggan",
	0x00007085:"yesclick",
	0x00007157:"withouse",
	0x000071DC:"woodsman",
	0x000099FE:"2artifact",
	0x00009CBC:"2ndparton",
	0x0000a1bc:"S.04",
	0x0000A23C:"1stparton",
	0x0000C7B4:"barbarian",
	0x0000c942:"S.10",
	0x0000C976:"alchemist",
	0x0000C993:"challenge",
	0x0000CAEF:"fakeplace",
	0x0000CD1E:"betrothed",
	0x0000CE84:"bodyguard",
	0x0000D02D:"artifact1",
	0x0000D02E:"artifact2",
	0x0000D02F:"artifact3",
	0x0000D030:"artifact4",
	0x0000D075:"bookstore",
	0x0000D0A4:"competior",
	0x0000D0D8:"mageguild",
	0x0000D0DF:"magicitem",
	0x0000D2CC:"kidnapper",
	0x0000D33C:"givetoken",
	0x0000D4BC:"informant",
	0x0000D4F6:"keptmetal",
	0x0000D50F:"dummymage",
	0x0000D51F:"pchasitem",
	0x0000D588:"guildhall",
	0x0000D6B7:"safehouse",
	0x0000D6EF:"itemplace",
	0x0000D738:"messenger",
	0x0000D742:"qgclicked",
	0x0000D7BF:"realmummy",
	0x0000D80C:"patsagent",
	0x0000D8D3:"extratime",
	0x0000D95F:"religitem",
	0x0000D9DA:"lordsmail",
	0x0000D9F0:"lovechild",
	0x0000DA2C:"huntstart",
	0x0000DAB7:"lovehouse",
	0x0000DBD3:"scorpions",
	0x0000DCD7:"vamphouse",
	0x0000DCED:"vamprelic",
	0x0000DD2E:"vamprival",
	0x0000DD50:"vampproof",
	0x0000DF69:"villainss",
	0x0000DFD7:"prophouse",
	0x0000E07D:"questdone",
	0x0000E0E3:"questtime",
	0x0000E1E3:"totaltime",
	0x0000E383:"towertime",
	0x0000E417:"townhouse",
	0x0000E627:"wrongdung",
	0x00018F34:"daedralord",
	0x0001928F:"agentplace",
	0x000195EF:"battlemage",
	0x00019717:"childhouse",
	0x00019765:"clearclick",
	0x00019AF7:"fatherdung",
	0x00019C69:"depository",
	0x00019F47:"dragonling",
	0x00019FC9:"apothecary",
	0x00019FCD:"firedaedra",
	0x00019FD4:"dispatcher",
	0x0001A193:"escapetime",
	0x0001A1C8:"competitor",
	0x0001A20B:"gimmegimme",
	0x0001A30C:"magicsword",
	0x0001A318:"magesguild",
	0x0001A415:"aurielsbow",
	0x0001A4B8:"gettraitor",
	0x0001A654:"givereward",
	0x0001A90C:"ingredient",
	0x0001A910:"hitseducer",
	0x0001AA28:"dummydarkb",
	0x0001AA4F:"founditem1",
	0x0001AA50:"founditem2",
	0x0001AA6F:"pchasitem1",
	0x0001AA70:"pchasitem2",
	0x0001AA71:"pchasitem3",
	0x0001AAB8:"hittraitor",
	0x0001ABA0:"pcgetsgold",
	0x0001ABC0:"guildmaker",
	0x0001ACFC:"readletter",
	0x0001AD31:"nightblade",
	0x0001ADD7:"rebelhouse",
	0x0001ADF7:"itemindung",
	0x0001B042:"npcclicked",
	0x0001B0B7:"noblehouse",
	0x0001B12F:"pickupitem",
	0x0001B29A:"shamandead",
	0x0001B4FB:"qgiverhome",
	0x0001B674:"sheogorath",
	0x0001B78F:"thiefplace",
	0x0001B797:"thiefhouse",
	0x0001B7D3:"teleportpc",
	0x0001B924:"vampleader",
	0x0001B9AE:"vampkilled",
	0x0001BA94:"vampreward",
	0x0001BAF3:"rippername",
	0x0001BCD3:"shortdelay",
	0x0001BEEC:"spellsword",
	0x0001C185:"werewolves",
	0x0001C18C:"questgiver",
	0x0001C18C:"tranporter",
	0x0001C1E3:"traveltime",
	0x0001C3D7:"witchhouse",
	0x0001C7B7:"storehouse",
	0x0001C928:"stronghold",
	0x00027D1C:"2shedungent",
	0x00028FB7:"2storehouse",
	0x00031BC2:"daedclicked",
	0x000327F6:"alchemyshop",
	0x00032BF2:"ancientlich",
	0x00032C1C:"darkbmember",
	0x00032E49:"childlocale",
	0x0003342C:"clickqgiver",
	0x000337D2:"iceatronach",
	0x000338CC:"bloodfather",
	0x00033BA0:"destination",
	0x00033FEF:"hidingplace",
	0x000341B8:"findtraitor",
	0x00034417:"contactdung",
	0x00034C7C:"givenletter",
	0x00034E77:"givershouse",
	0x00034FF4:"hitguardian",
	0x0003544D:"dummydaedra",
	0x00035717:"hookerhouse",
	0x00035A0D:"frostdaedra",
	0x00035C48:"lettergiven",
	0x000362B2:"pickuplocal",
	0x000365F7:"scholardung",
	0x000365FE:"relartifact",
	0x00036C57:"targethouse",
	0x00036F1C:"thiefmember",
	0x000371C2:"vampclicked",
	0x00037697:"ripperhouse",
	0x00037BF7:"victimhouse",
	0x00037C14:"queenreward",
	0x0003815A:"traitordead",
	0x0003844C:"transporter",
	0x00063E8B:"daedraprince",
	0x000666A9:"falseletter1",
	0x000666AA:"falseletter2",
	0x000666AB:"falseletter3",
	0x000666AC:"falseletter4",
	0x000668A7:"clickonenemy",
	0x0006799C:"finddaughter",
	0x000685D2:"fireatronach",
	0x00068642:"enemyclicked",
	0x00069178:"aurielshield",
	0x0006A3EF:"meetingplace",
	0x0006B2C7:"mensclothing",
	0x0006B48D:"lesserdaedra",
	0x0006BC6F:"pickedupitem",
	0x0006C4D2:"ironatronach",
	0x0006C638:"pickupregion",
	0x0006CD2E:"hunterkilled",
	0x0006CF75:"oracletemple",
	0x0006D40B:"mistresshome",
	0x0006e2bd:"scourgbarrow",
	0x0006E38F:"sleepingmage",
	0x0006E698:"thievesguild",
	0x00070077:"sistershouse",
	0x00070CC2:"rulerclicked",
	0x000C7C90:"daedraseducer",
	0x000CC097:"daughterhouse",
	0x000CCFB0:"clickoblivion",
	0x000CD2EC:"clickonqgiver",
	0x000CD81B:"betrothedhome",
	0x000D0AD2:"fleshatronach",
	0x000D9A14:"scholarreward",
	0x000D9D5F:"religiousitem",
	0x000D9EB8:"missingperson",
	0x000DB798:"skeffingcoven",
	0x000E0914:"traitorreward",
	0x000E0DF6:"questfinished",
	0x00199CF4:"betrayguardian",
	0x001A5D0C:"giveingredient",
	0x001A9C53:"executiondelay",
	0x001B6FBB:"revealmonsters",
	0x001C82C7:"womensclothing",
	0x00358AC2:"oblivionclicked",
	0x000199B3:"S.10",
	0x00006CC3:"S.13",
	0x00006CC3:"S.05",
	0x0006E0C3:"UNKNAME_0006E0C3",
	0x0001B38D:"UNKNAME_0001B38D",
	0x00068071:"UNKNAME_00068071",
	0x00006A83:"UNKNAME_00006A83",
	0x00019983:"UNKNAME_00019983",
	0x0001BD43:"UNKNAME_0001BD43",
	0x0001A1B4:"UNKNAME_0001A1B4",
	0x0000E0EC:"UNKNAME_0000E0EC",
	0x0001B163:"UNKNAME_0001B163",
	0x000343A8:"UNKNAME_000343A8",
	0x00003660:"UNKNAME_00003660",
	0x0001BB33:"UNKNAME_0001BB33",
	0x0001BD43:"UNKNAME_0001BD43",
	0x0000D533:"UNKNAME_0000D533",
	0x00004F37:"UNKNAME_00004F37",
	0x000281FC:"UNKNAME_000281FC",
	0x00004F37:"UNKNAME_00004F37",
	0x000066B0:"UNKNAME_000066B0",
	0x00004C5A:"UNKNAME_00004C5A",
	0x00000D27:"UNKNAME_00000D27",
	0x000141BA:"UNKNAME_000141BA",
	0x00001A80:"UNKNAME_00001A80",
	0x000269FC:"UNKNAME_000269FC",
	0x00004F37:"UNKNAME_00004F37",
	0x00009D7C:"UNKNAME_00009D7C",
	0x0000A03C:"UNKNAME_0000A03C",
	0x00004F37:"UNKNAME_00004F37",
	0x0001347C:"UNKNAME_0001347C",
	0x00002657:"UNKNAME_00002657",
	0x000288BC:"UNKNAME_000288BC",
	0x00013875:"UNKNAME_00013875",
	0x000096FC:"UNKNAME_000096FC",
	0x0000A03C:"UNKNAME_0000A03C",
	0x00034BD0:"UNKNAME_00034BD0",
	0x0001BC70:"UNKNAME_0001BC70",
	0x0001C6D3:"UNKNAME_0001C6D3",
	0x000665B8:"UNKNAME_000665B8",
	0x00035BD3:"UNKNAME_00035BD3",
	0x0001B57A:"UNKNAME_0001B57A",
	0x00034273:"UNKNAME_00034273",
	0x00035BD3:"UNKNAME_00035BD3",
	0x00006EA3:"UNKNAME_00006EA3",
	0x000096FC:"UNKNAME_000096FC",
	0x0004D53C:"UNKNAME_0004D53C",
	0x000DA513:"UNKNAME_000DA513",
	0x00001941:"UNKNAME_00001941",
	0x00001942:"UNKNAME_00001942",
	0x00001943:"UNKNAME_00001943",
	0x00006CC3:"UNKNAME_00006CC3",
	0x0001BF33:"UNKNAME_0001BF33",
	0x0000353D:"UNKNAME_0000353D",
	0x0000353E:"UNKNAME_0000353E",
	0x0000353F:"UNKNAME_0000353F",
	0x00003540:"UNKNAME_00003540",
	0x0003665D:"UNKNAME_0003665D",
	0x0000E0EC:"UNKNAME_0000E0EC",
	0x000038D9:"UNKNAME_000038D9",
	0x0000060A:"UNKNAME_0000060A",
	0x00001999:"UNKNAME_00001999",
	0x00028BFC:"UNKNAME_00028BFC",
	0x000DE747:"UNKNAME_000DE747",
	0x0001C0AE:"UNKNAME_0001C0AE",
	0x0000095D:"UNKNAME_0000095D",
	0x0013EAEF:"UNKNAME_0013EAEF",
	0x00012DF5:"UNKNAME_00012DF5",
	0x001B3ECB:"UNKNAME_001B3ECB",
	0x00004F37:"UNKNAME_00004F37",
	0x0001BEB3:"UNKNAME_0001BEB3",
	0x000D1F34:"UNKNAME_000D1F34",
	0x000D1F1B:"UNKNAME_000D1F1B",
	0x000D1F7C:"UNKNAME_000D1F7C",
	0x000D1FF5:"UNKNAME_000D1FF5",
	0x001A3FEF:"UNKNAME_001A3FEF",
	0x000D1F4D:"UNKNAME_000D1F4D",
	0x00066043:"UNKNAME_00066043",
	0x000271BC:"UNKNAME_000271BC",
	0x0000DD26:"UNKNAME_0000DD26",
	0x00068563:"UNKNAME_00068563",
	0x00096CFC:"UNKNAME_00096CFC",
	0x000A02BD:"UNKNAME_000A02BD",
	0x0001A175:"UNKNAME_0001A175",
	0x001AF3BD:"UNKNAME_001AF3BD",
	0x0001C326:"UNKNAME_0001C326",
	0x000018D8:"UNKNAME_000018D8",
	0x00035FB2:"UNKNAME_00035FB2",
	0x00006CF0:"UNKNAME_00006CF0",
	0x000DA06C:"UNKNAME_000DA06C",
	0x00006A20:"UNKNAME_00006A20",
	0x000DA06C:"UNKNAME_000DA06C",
	0x00006A20:"UNKNAME_00006A20",
	0x000DA06C:"UNKNAME_000DA06C",
	0x00006A20:"UNKNAME_00006A20",
	0x000DA06C:"UNKNAME_000DA06C",
	0x00006A20:"UNKNAME_00006A20",
	0x000DA06C:"UNKNAME_000DA06C",
	0x00006A20:"UNKNAME_00006A20",
	0x0001C1D3:"UNKNAME_0001C1D3",
	0x00035BD3:"UNKNAME_00035BD3",
	0x0001C1D3:"UNKNAME_0001C1D3",
	0x0001C393:"UNKNAME_0001C393",
	0x000342F3:"UNKNAME_000342F3",
	0x0001C1D3:"UNKNAME_0001C1D3",
	0x0001C393:"UNKNAME_0001C393",
	0x00006B23:"UNKNAME_00006B23",
	0x0001A173:"UNKNAME_0001A173",
	0x00003572:"UNKNAME_00003572",
	0x00006B73:"UNKNAME_00006B73",
	0x0000DB1C:"UNKNAME_0000DB1C",
	0x001C3A54:"UNKNAME_001C3A54",
	0x0004DCFC:"UNKNAME_0004DCFC",
	0x0009EB7C:"UNKNAME_0009EB7C",
	0x00009BAE:"UNKNAME_00009BAE",
	0x0006B98D:"UNKNAME_0006B98D",
	0x0000D7B9:"UNKNAME_0000D7B9",
	0x0000D20C:"UNKNAME_0000D20C",
	0x0000D37E:"UNKNAME_0000D37E",
	0x0001C7CC:"UNKNAME_0001C7CC",
	0x000349E5:"UNKNAME_000349E5",
	0x00034712:"UNKNAME_00034712"
}

SECTION_ITEM = 0
SECTION_1 = 1
SECTION_2 = 2
SECTION_NPC = 3
SECTION_LOCATION = 4
SECTION_5 = 5
SECTION_TIMER = 6
SECTION_MOB = 7
SECTION_OPC = 8
SECTION_STATE = 9
SECTION_TVA = 10

class QItem:
	RewardEnum = [
		"artifact",
		"item",
		"gold",
		"unknown"
		]
		
	def GetName(self):
		if self.TVH not in TVH_MAP:
			name = "%08x"%self.TVH
		else:
			name = "_"+TVH_MAP[self.TVH]+"_"
		return name
		
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_ITEM)+self.id*0x13)
		(self.intID, self.reward, self.category, self.catIdx, self.TVH, self.ObjPtr, self.t1, self.t2) = struct.unpack('<HB2H2I2H', self.f.read(0x13))
	
	def TemplateText(self):
		return "Item %s %s"%(self.GetName(), self.RewardEnum[self.reward])
		
	def toString(self):
		return "Item %d : \n"\
			  "\t id : %d\n"\
			  "\t reward : %s\n"\
			  "\t category : %02x\n"\
			  "\t catIdx : %04x\n"\
			  "\t TVH : %s\n"\
			  "\t ObjPtr : %08x\n"\
			  "\t text1 : %04x\n"\
			  "\t text2 : %04x\n"%(self.id, self.intID, self.RewardEnum[self.reward], self.category, self.catIdx, self.GetName(), self.ObjPtr, self.t1, self.t2)
			  
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()
		
class QLoc:
	GenLocEnm = [
		"specific",
		"local",
		"remote"]
	
	FineLocEnum = [
		"building",
		"dungeon"]	
		
	def GetName(self):
		if self.TVH not in TVH_MAP:
			name = "%08x"%self.TVH
		else:
			name = "_"+TVH_MAP[self.TVH]+"_"
		return name
		
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_LOCATION)+self.id*0x18)
		(self.intID, self.flag, self.genLoc, self.fineLoc, self.type, self.doorSel, self.unkA, self.TVH, self.Obj, self.t1, self.t2) = struct.unpack('<H2B4H2I2H', self.f.read(0x18))
	
	def TemplateText(self):
		s =  "Place %s %s %d"%(self.GetName(), self.GenLocEnm[self.genLoc], self.fineLoc)
		if self.type == 0xFFFF:
			s += " random"
		return s
		
	def toString(self):
		
		return "Location %d : \n"\
			  "\t id : %d\n"\
			  "\t flag : x%02x\n"\
			  "\t generalLoc : %02x\n"\
			  "\t fineLoc : %04x\n"\
			  "\t type : %04x\n"\
			  "\t doorSelector : %04x\n"\
			  "\t unkA : %08x\n"\
			  "\t TVH : %s\n"\
			  "\t Obj : %08x\n"\
			  "\t text1 : %04x\n"\
			  "\t text2 : %04x\n"%(self.id, self.intID, self.flag, self.genLoc, self.fineLoc, self.type, self.doorSel, self.unkA, self.GetName(), self.Obj, self.t1, self.t2)
			  
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()
		
class QNPC:
	def GetName(self):
		if self.TVH not in TVH_MAP:
			name = "%08x"%self.TVH
		else:
			name = "_"+TVH_MAP[self.TVH]+"_"
		return name
		
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_NPC)+self.id*0x14)
		(self.intID, self.gender, self.facePicID, self.unk4, self.factionID, self.TVH, self.obj, self.t1, self.t2) = struct.unpack('<H2B2H2I2H', self.f.read(0x14))
	

	def GetSex(self):
		if self.gender == 0:
			return "male"
		elif self.gender == 1:
			return "female"
		else :
			return "random"
			
	def TemplateText(self):
		return "Person %s face %d group %d %s"%(self.GetName(), self.facePicID,  self.factionID, self.GetSex())
		
	def toString(self):
		return "NPC %d : \n"\
			  "\t id : %d\n"\
			  "\t gender : x%02x\n"\
			  "\t facePicture : %02x\n"\
			  "\t unk4 : %04x\n"\
			  "\t factionID : %04x\n"\
			  "\t TVH : %s\n"\
			  "\t Obj : %08x\n"\
			  "\t text1 : %04x\n"\
			  "\t text2 : %04x\n"%(self.id, self.intID, self.gender, self.facePicID, self.unk4, self.factionID, self.GetName(), self.obj, self.t1, self.t2)
			  
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()

class QMob:
	def GetName(self):
		if self.TVH not in TVH_MAP:
			name = "%08x"%self.TVH
		else:
			name = "_"+TVH_MAP[self.TVH]+"_"
		return name
		
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_MOB)+self.id*0xe)
		(self.intID, self.unk, self.type, self.count, self.TVH, self.obj) = struct.unpack('<BHBHII', self.f.read(0xe))
			
	def TemplateText(self):
		return "Foe %s type:%d count:%d"%(self.GetName(), self.type,  self.count)
		
	def toString(self):
		return "MOB %d : \n"\
			  "\t id : %d\n"\
			  "\t unk : %04x\n"\
			  "\t type : %02x\n"\
			  "\t count : %04x\n"\
			  "\t TVH : %s\n"\
			  "\t Obj : %08x\n"%(self.id, self.intID, self.unk, self.type, self.count, self.GetName(), self.obj)
			  
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()
		
class QTimer:
	TIMER_TYPES = ['TIMER_RANDOM',
				'TIMER_SIMPLE',
				'TIMER_1REF',
				'TIMER_2REF_FROMTO',
				'TIMER_1REF',
				'TIMER_2REF_2DEST']
	
	FLAGS = {
		0x0001:"DEFAULT",
		0x0002:"RESET_AFTER_TRIGGER",
		0x0004:"FLIP_FLOP",
		0x0008:"AUTO_RESTART",
		0x0010:"AND_BACK",
		0x0040:"RUNNING"
		}
		
	def GetName(self):
		if self.TVH not in TVH_MAP:
			name = "0x%08X"%self.TVH
			# print('%s:"UNKNAME_%08X",'%(name, self.TVH))
		else:
			name = "_"+TVH_MAP[self.TVH]+"_"
		return name
	
	def GetFlagsAsStr(self):
		arr = []
		for k in self.FLAGS:
			if self.flags & k:
				arr.append(self.FLAGS[k])
		return "|".join(arr)
			
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_TIMER)+self.id*0x21)
		(self.intID, self.flags, self.type, self.min, self.max, self.start, self.dur, self.l1, self.l2, self.TVH) = struct.unpack('<2hb7i', self.f.read(0x21))
		
		if self.type >= 2 :
			if self.flags & 0x100 :
				self.l1Obj = QNPC(self.f, self.q, self.l1)
			else:
				self.l1Obj = QLoc(self.f, self.q, self.l1)
				
		if self.type == 3 or self.type == 5:
			if self.flags & 0x200 :
				self.l2Obj = QNPC(self.f, self.q, self.l2)
			else:
				self.l2Obj = QLoc(self.f, self.q, self.l2)
				
	def toString(self):
		
		return "Timer %d : \n"\
			  "\t id : %d\n"\
			  "\t flags : %s\n"\
			  "\t type : %s\n"\
			  "\t min : %d\n"\
			  "\t max : %d\n"\
			  "\t started@ : %08x\n"\
			  "\t duration : %08x\n"\
			  "\t link1 : %08x\n"\
			  "\t link2 : %08x\n"\
			  "\t TVH : %s\n"%(self.id, self.intID, self.GetFlagsAsStr(), self.TIMER_TYPES[self.type], self.min, self.max, self.start, self.dur, self.l1, self.l2, self.GetName())
	
	def TemplateText(self):
		if self.type < 2:
			return "ClassicClock %s %s %d %d flags:%s"%(self.GetName(), self.TIMER_TYPES[self.type], self.min, self.max, self.GetFlagsAsStr())
		elif self.type == 2 or self.type == 4:
			return "ClassicClock %s %s %d %d flags:%s ref:%s"%(self.GetName(), self.TIMER_TYPES[self.type], self.min, self.max, self.GetFlagsAsStr(), self.l1Obj.GetName())
		else:
			return "ClassicClock %s %s %d %d flags:%s refs:%s %s"%(self.GetName(), self.TIMER_TYPES[self.type], self.min, self.max, self.GetFlagsAsStr(), self.l1Obj.GetName(), self.l2Obj.GetName())
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()
	
class QState:
	def GetName(self):
		if self.TVH not in TVH_MAP:
			name = "%08x"%self.TVH
		else:
			name = "_"+TVH_MAP[self.TVH]+"_"
		return name
		
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_STATE)+self.id*0x8)
		(self.intID, self.isGlobal, self.globIdx, self.TVH) = struct.unpack('<H2BI', self.f.read(0x8))
		
	def toString(self):
		return "State %d : \n"\
			  "\t id : %d\n"\
			  "\t isGlobal : x%02x\n"\
			  "\t globalIdx/state : %02x\n"\
			  "\t TVH : %s\n"%(self.id, self.intID, self.isGlobal, self.globIdx, self.GetName())
			  
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()	

class QOpcArg:
	SectionEnum = [
		"Item",
		"UNK1",
		"UNK2",
		"Npc",
		"Location",
		"UNK5",
		"Timer",
		"Mob",
		"Script",
		"State"
		]
		
	def toString(self):
		if self.local != 0x12345678:
			if self.field7 == 0xFFFFFFFF or self.field7 == 0xFFFFFFFE:
				n = "None"
			elif self.sectionId == SECTION_ITEM:
				n = self.opc.q.items[self.field7].GetName()
			elif self.sectionId == SECTION_NPC:
				n = self.opc.q.npc[self.field7].GetName()
			elif self.sectionId == SECTION_LOCATION:
				n = self.opc.q.locations[self.field7].GetName()
			elif self.sectionId == SECTION_TIMER:
				n = self.opc.q.timers[self.field7].GetName()
			elif self.sectionId == SECTION_STATE:
				n = self.opc.q.states[self.field7].GetName()
			else:
				n = "%08x"%self.field7
				
			return "%02x %s %s\n"%(self.flags, self.SectionEnum[self.sectionId], n)
		else:
			return "%02x Const %08x\n"%(self.flags, self.field7)
		
	def __init__(self, data, father):
		self.opc = father
		(self.flags, self.local, self.sectionId, self.field7, self.fieldB) = struct.unpack('<BIHII', data)
		
class QOpc:
	OpcEnum = [
		"PlaceItemInLocation",
		"HasItemBeenDelivered",
		"SetStateAfterKillCount",
		"HasItemBeenFound",
		"Opc04",
		"Opc05",
		"EndQuest",
		"ClearStates",
		"Opc08",
		"Opc09",
		"Opc0A",
		"Opc0B",
		"StartTimer",
		"StopTimer",
		"Opc0E",
		"Opc0F",
		"Opc10",
		"Opc11",
		"Opc12",
		"AddLocToMap",
		"Opc14",
		"SetStateWhenMobHited",
		"PlaceMobAt",
		"Log",
		"Opc18",
		"Opc19",
		"Opc1A",
		"Opc1B",
		"SetStateWhenMeet",
		"Opc1D",
		"PlaceNpcAtLocation",
		"Opc1F",
		"Opc20",
		"Opc21",
		"Opc22",
		"Opc23",
		"Opc24",
		"Opc25",
		"Opc26",
		"Opc27",
		"Opc28",
		"Opc29",
		"Opc2A",
		"Opc2B",
		"Opc2C",
		"Opc2D",
		"HideNPC",
		"Opc2F",
		"Opc30",
		"Opc31",
		"Opc32",
		"DisplayMsg",
		"And",
		"Opc35",
		"Opc36",
		"Opc37",
		"Opc38",
		"Opc39",
		"Opc3A",
		"Opc3B",
		"Opc3C",
		"Opc3D",
		"Opc3E",
		"Opc3F",
		"Opc40",
		"Opc41",
		"Opc42",
		"Opc43",
		"Opc44",
		"Opc45",
		"Opc46",
		"Opc47",
		"Opc48",
		"Opc49",
		"Opc4A",
		"Opc4B",
		"Opc4C",
		"Opc4D",
		"Opc4E",
		"Opc4F",
		"Opc50",
		"Opc51",
		"Opc52",
		"Opc53",
		"Opc54",
		"Opc55",
		"Opc56",
		"Opc57"
		]
		
		
	def Parse(self):
		self.f.seek(self.q.GetSectionOff(SECTION_OPC)+self.id*0x57)
		(self.opcode, self.flags, self.paramCount) = struct.unpack('<3H', self.f.read(0x6))
		
		self.arg = [None] * 5
		for i in range(5):
			self.arg[i] = QOpcArg(self.f.read(0xF), self)
		
		(self.msgId, self.LastUpdate) = struct.unpack('<HI', self.f.read(6))
		
	

	def toString(self):
		s =  "%s flags:%04x Msg:%04x\n"%(self.OpcEnum[self.opcode], self.flags, self.msgId)
		for i in range(self.paramCount):
			s += "\t"+self.arg[i].toString()
		return s
			  
	def __init__(self, f, q, id):
		self.f = f
		self.q = q
		self.id = id
		self.Parse()
		
		
class Quest:
	def ParseHead(self, bPrint=False):
		header = self.f.read(0x10)
		(self.id, self.faction, self.res, self.resFile, self.dbg) = struct.unpack('3h9sB', header)
		if bPrint:
			print(self.toString())
		self.sectionCount = struct.unpack('10h', self.f.read(20))
		self.sectionOff = struct.unpack('10h', self.f.read(20))
	
	def ParseTimer(self, id, bPrint=False):
		timer = QTimer(self.f, self, id)
		if bPrint:
			print(timer.toString())
		return timer
		
	def ParseMob(self, id, bPrint=False):
		mob = QMob(self.f, self, id)
		if bPrint:
			print(mob.toString())
		return mob
		
	def ParseNPC(self,  id, bPrint=False):
		npc = QNPC(self.f, self, id)
		if bPrint:
			print(npc.toString())
		return npc
		
	def ParseLocation(self,  id, bPrint=False):
		loc = QLoc(self.f, self, id)
		if bPrint:
			print(loc.toString())
		return loc
		
	def ParseItem(self,  id, bPrint=False):
		item = QItem(self.f, self, id)
		if bPrint:
			print(item.toString())
		return item
		
	def ParseState(self,  id, bPrint=False):
		state = QState(self.f, self, id)
		if bPrint:
			print(state.toString())
		return state
		
	def ParseOpcode(self,  id, bPrint=False):
		opc = QOpc(self.f, self, id)
		if bPrint:
			print(opc.toString())
		return opc
	
	def ParseSections(self, bVerbose = False):
		if self.sectionCount[SECTION_ITEM] > 0 :
			if bVerbose:
				print("Item Section @%02x, count %d\n"%(self.sectionOff[SECTION_ITEM], self.sectionCount[SECTION_ITEM]))
			for i in range(self.sectionCount[SECTION_ITEM]):
				self.items[i] = self.ParseItem(i)
				
		if self.sectionCount[SECTION_NPC] > 0 : 
			if bVerbose:
				print("NPC Section @%02x, count %d\n"%(self.sectionOff[SECTION_NPC], self.sectionCount[SECTION_NPC]))
			for i in range(self.sectionCount[SECTION_NPC]):
				self.npc[i] = self.ParseNPC(i)
				
		if self.sectionCount[SECTION_LOCATION] > 0 : 
			if bVerbose:
				print("Location Section @%02x, count %d\n"%(self.sectionOff[SECTION_LOCATION], self.sectionCount[SECTION_LOCATION]))
			for i in range(self.sectionCount[SECTION_LOCATION]):
				self.locations[i] = self.ParseLocation(i)
				
		if self.sectionCount[SECTION_TIMER] > 0 : 
			if bVerbose:
				print("Timer Section @%02x, count %d\n"%(self.sectionOff[SECTION_TIMER], self.sectionCount[SECTION_TIMER]))
			for i in range(self.sectionCount[SECTION_TIMER]):
				self.timers[i] = self.ParseTimer(i)
				
		if self.sectionCount[SECTION_MOB] > 0 : 
			if bVerbose:
				print("Mob Section @%02x, count %d\n"%(self.sectionOff[SECTION_TIMER], self.sectionCount[SECTION_MOB]))
			for i in range(self.sectionCount[SECTION_MOB]):
				self.mobs[i] = self.ParseMob(i)
		
		if self.sectionCount[SECTION_STATE] > 0 : 
			if bVerbose:
				print("State Section @%02x, count %d\n"%(self.sectionOff[SECTION_STATE], self.sectionCount[SECTION_STATE]))
			for i in range(self.sectionCount[SECTION_STATE]):
				self.states[i] = self.ParseState(i)
		
		if self.sectionCount[SECTION_OPC] > 0 : 
			if bVerbose:
				print("Script Section @%02x, count %d\n"%(self.sectionOff[SECTION_OPC], self.sectionCount[SECTION_OPC]))
			for i in range(self.sectionCount[SECTION_OPC]):
				self.script[i] = self.ParseOpcode(i)
	
	def PrintAll(self):
		for item in self.items:
			print item.TemplateText()
		
		print("")
		for npc in self.npc:
			print npc.TemplateText()
			
		print("")	
		for loc in self.locations:
			print loc.TemplateText()
		
		print("")	
		for mob in self.mobs:
			print mob.TemplateText()
			
		print("")	
		for timer in self.timers:
			print timer.TemplateText()
		
		print("")
		print "Quest Script\n"
		for opc in self.script:
			print opc.toString()
			
		# print("")	
		# for state in self.states:
			# print state.toString()
	
	def PrintClocksAsText(self):
		for timer in self.timers:
			print("\t"+timer.TemplateText())
			
	def GetSectionOff(self, section):
		return self.sectionOff[section]
		
	def toString(self):
		return "Header \n"\
				  "\t ID: %d\n"\
				  "\t FactionID: %d \n"\
				  "\t ResID : %d\n"\
				  "\t ResFile : %s\n"\
				  "\t bHasDBG : %d\n"%(self.id, self.faction, self.res, self.resFile, self.dbg)
				  
	def __init__(self, f):
		self.f = f
		self.ParseHead()

		self.items = [None] * self.sectionCount[SECTION_ITEM]
		self.npc = [None] * self.sectionCount[SECTION_NPC]
		self.locations = [None] * self.sectionCount[SECTION_LOCATION]
		self.timers = [None] * self.sectionCount[SECTION_TIMER]
		self.mobs = [None] * self.sectionCount[SECTION_MOB]
		self.states = [None] * self.sectionCount[SECTION_STATE]
		self.script = [None] * self.sectionCount[SECTION_OPC]
	


	
		  
def ParseFile(name):
	f =  open(name, 'rb')
	if f == None:
		print("[ERR] cannot open %s"%name)
	else:
		print(name)
		q = Quest(f)
		q.ParseSections()
		#q.PrintClocksAsText()
		q.PrintAll()
		print("")
		

def ParseFolder(path):
	dir =  os.listdir(path)
	if dir == None:
		print("[ERR] cannot open %s"%name)
	else:
		for file in dir:
			if ".QBN" in file:
				ParseFile(path+"\\"+file)

def Hash(s):
	h = 0
	for c in s:
		h = ord(c) + (h<<1)
	print "hash : %08x"%h
	
def help():
	print("USAGE : QBN_timer.py d FOLDER")
	print("USAGE : QBN_timer.py f FILENAME")
	print("USAGE : QBN_timer.py h STRING")
		
def main():
	if len(sys.argv) < 3:
		help()
	elif sys.argv[1] == "d":
		ParseFolder(sys.argv[2])
	elif sys.argv[1] == "f":
		ParseFile(sys.argv[2])
	elif sys.argv[1] == "h":
		Hash(sys.argv[2])
	else:
		help()

main()
