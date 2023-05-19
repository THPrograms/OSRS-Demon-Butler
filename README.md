# OSRS Demon Butler

OSRS Demon Butler is a discord bot written in python, allowing Discord users to pull their Old School HiScores stats directly into Discord.

## Adding To Your Discord Channel

To add OSRS Demon Butler to your discord server, click the link below:

[https://discord.com/api/oauth2/authorize?client_id=907075956877959170&permissions=534723950656&scope=bot](https://discord.com/api/oauth2/authorize?client_id=907075956877959170&permissions=534723950656&scope=bot)

## Discord Commands

### HiScores Stat Monitor Commands:

#### - !Register [OSRS Username]

Registers provided Username to receive updates when they level-up a skill, or increase KC on a boss. The update will be sent in the channel that this command is sent in. I suggest creating a channel for this if using this feature.

![register](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/138634dc-d7bc-429d-be05-aa1f37b9c806)

#### - !Unregister [OSRS Username]

Unregisters provided username from the stat monitor for ALL channels in the server the command is sent in.

![unregister](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/938a453e-7c69-4d39-abb2-c3121879844d)

#### - !Registered

Provides a list of users that are registered in ALL channels in the server the command is sent in.

![registered](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/46486342-60f0-49cc-8a1e-bb8a531b02a2)

#### - !Migrate [Channel ID]

Migrates all users registered in provided channel ID to the channel the command is sent in and unregisters them from the channel provided.

![migrate](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/b2f09d59-3912-4df3-bb5b-cc571b8bb859)

#### - !Copy [Channel ID]

Functionally similar to the migrate command. Does not unregister users from the provided channel.

![copy](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/8c514a61-08d8-403a-9571-78ec62007059)

### HiScores Stat Pull Commands:

#### !Player [OSRS Username]

Returns a message displaying the provided player's stats on the [Old School Hiscores](https://secure.runescape.com/m=hiscore_oldschool/overall) in the channel the command was sent in.

![player](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/e100e301-a521-480d-a691-9c599afb6152)

#### !Skill [Skill] [OSRS Username]

Returns a message displaying the provided player's stats for the provided skill in the channel the command was sent in.

![skill](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/69605442-8ae2-4727-a4ba-d92939c9c9a9)

#### !KC [Boss/Minigame] [OSRS Username]

Returns a message displaying the provided player's stats for the provided boss/minigame in the channel the command was sent in.

![kc](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/3ee9a076-4ce5-490e-9e87-e2015a8075ee)

### General Commands:

#### !Help

Returns a message displaying the various commands in the channel the command was sent in.

#### !Suggest [Suggestion]

Opens an Issue in the github project. Please use this to make any suggestions or report any bugs about the bot.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[MIT](https://github.com/THPrograms/OSRS-Demon-Butler/blob/main/LICENSE)
