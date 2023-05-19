# OSRS Demon Butler

OSRS Demon Butler is a discord bot written in python, allowing Discord users to pull their Old School HiScores stats directly into Discord.

## Adding To Your Discord Channel

To add OSRS Demon Butler to your discord server, click the link below:

[https://discord.com/api/oauth2/authorize?client_id=907075956877959170&permissions=534723950656&scope=bot](https://discord.com/api/oauth2/authorize?client_id=907075956877959170&permissions=534723950656&scope=bot)

## Discord Commands

### HiScores Stat Monitor Commands:

#### - !Register [OSRS Username]

Registers provided Username to receive updates when they level-up a skill, or increase KC on a boss. The update will be sent in the channel that this command is sent in. I suggest creating a channel for this if using this feature.

![register](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/87cb01dd-edd3-48aa-9d38-801ba9e2ab57)


#### - !Unregister [OSRS Username]

Unregisters provided username from the stat monitor for ALL channels in the server the command is sent in.

![unregister](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/938a453e-7c69-4d39-abb2-c3121879844d)

#### - !Registered

Provides a list of users that are registered in ALL channels in the server the command is sent in.

![registered](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/db665dbf-c9cf-4193-a17a-c140909ec2a9)

#### - !Migrate [Channel ID]

Migrates all users registered in provided channel ID to the channel the command is sent in and unregisters them from the channel provided.

![migrate](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/8c8f1873-55b5-4319-a83f-dc35ad34f513)

#### - !Copy [Channel ID]

Functionally similar to the migrate command. Does not unregister users from the provided channel.

![copy](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/a440796e-d02c-48d6-b6cf-070915ca727f)

### HiScores Stat Pull Commands:

#### !Player [OSRS Username]

Returns a message displaying the provided player's stats on the [Old School Hiscores](https://secure.runescape.com/m=hiscore_oldschool/overall) in the channel the command was sent in.

![player](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/08a81ec4-90ae-40fe-8bbe-0644535afb56)

#### !Skill [Skill] [OSRS Username]

Returns a message displaying the provided player's stats for the provided skill in the channel the command was sent in.

![skill](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/30164fa3-64ee-437f-b2ba-57805aaa26f9)

#### !KC [Boss/Minigame] [OSRS Username]

Returns a message displaying the provided player's stats for the provided boss/minigame in the channel the command was sent in.

![kc](https://github.com/THPrograms/OSRS-Demon-Butler/assets/117711510/0bf55601-5849-496a-96b1-1fd6d1cd586f)

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
