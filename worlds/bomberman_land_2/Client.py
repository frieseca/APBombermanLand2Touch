from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


BIZHAWK_ARM9_DOMAIN = "ARM9 System Bus"



class BombermanLand2Client(BizHawkClient):
    game = "Bomberman Land Touch! 2"
    system = "NDS"
    patch_suffix = ".apextension"
    items_handling = 0b111
    last_received_item = 0


    async def distribute_pieces(self, ctx: "BizHawkClientContext", items_received, read_results) -> None:
        star_count = sum(1 for n in items_received if n.item == 1) #counts star pieces
        if star_count >16:
            star_count = star_count-16
            star_mask = (1 << star_count) - 1
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7A8, 0xFF.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7A9, 0xFF.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7AA, star_mask.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
        elif star_count > 8:
            star_count = star_count - 8
            star_mask = (1 << star_count) - 1
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7A8, 0xFF.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7A9, star_mask.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7AA, 0x00.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
        else:
            star_mask = (1 << star_count) - 1
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7A8, star_mask.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7A9, 0x00.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7AA, 0x00.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])

        earth_count = sum(1 for n in items_received if n.item == 4) #counts earth pieces
        if earth_count >16:
            earth_count = earth_count-16
            earth_mask = (1 << earth_count) - 1
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B4, 0xFF.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B5, 0xFF.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B6, earth_mask.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
        elif earth_count > 8:
            earth_count = earth_count - 8
            earth_mask = (1 << earth_count) - 1
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B4, 0xFF.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B5, earth_mask.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B6, 0x00.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
        else:
            earth_mask = (1 << earth_count) - 1
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B4, earth_mask.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B5, 0x00.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
            await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7B6, 0x00.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])

    async def calc_tokens(self, ctx: "BizHawkClientContext", items_received, read_results) -> None:
        token_count = 0
        for byte in read_results[272:312]:
            if byte & 0x04:
                token_count += 1
        print("Post minigame count:", token_count)
        tokens_received = sum(1 for n in items_received if n.item == 8)  # counts tokens pieces
        token_count = token_count + tokens_received
        triple_received = sum(1 for n in items_received if n.item == 9) #counts triple tokens
        token_count = token_count + triple_received * 3
        print("Post received count:",token_count)
        for location in ctx.checked_locations:
            print("checked locations", ctx.checked_locations)
            if location == 5 and token_count>0:
                token_count = token_count - 1
        print("post shop count",token_count)
        await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE7C0, token_count.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])

    async def give_items(self, ctx: "BizHawkClientContext", items_received, read_results) -> None:
        bomb = 0
        aquabomb = 0
        broom = 0
        for item in items_received:
            if item.item == 24: bomb = 1
            if item.item == 14: aquabomb = 1
            if item.item == 20: broom += 1

        first_item_byte = (
            0x00
        )
        if broom < 2:
            second_item_byte = (
                (bomb<<6) |
                (broom<<2)
            )
        else:
            second_item_byte = (
                (bomb<<6) |
                (1<<2)|
                (1<<4) ## need to add in logic for fire vs water
            )
        third_item_byte = (
            (aquabomb<<4)
        )
        await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE8E0, first_item_byte.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE8E1, second_item_byte.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])
        await bizhawk.write(ctx.bizhawk_ctx, [(0x20AE8E2, third_item_byte.to_bytes(1, "little"), BIZHAWK_ARM9_DOMAIN)])

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            #rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0, 12, "ROM")]))[0]).decode("ascii")
            print("ROM NAME:",rom_name)
            if rom_name != "TCHBMBMNLND2":
                return False  # Not a MYGAME ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        # This is a MYGAME ROM
        ctx.game = self.game
        ctx.items_handling = 0b111
        ctx.want_slot_data = True
        print("We got through the validate rom check")
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Read save data
            save_data = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x20AE7A0, 512, BIZHAWK_ARM9_DOMAIN)]
            ))[0]

            #print(save_data)
            #print(save_data[8])
            #print(save_data[32])
            #print(save_data[8] & 0x40)
            # Check locations

            #Jumping Rope
            if save_data[268] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [1]
                }])
            #bending spoons
            if save_data[276] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [2]
                }])
            #Star Castle A Chest 1
            if save_data[82] & 0x08:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [3]
                }])
            #Star Castle A Chest 2
            if save_data[82] & 0x10:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [4]
                }])
            #worn broom bought
            if save_data[339] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [5]
                }])
            #Star B Shakeable Tree
            if save_data[76] & 0x20:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [6]
                }])
            #Acrobat Wheel
            if save_data[270] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [7]
                }])
            #Bomber House Star
            if save_data[313] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [8]
                }])
            #Fortune Token Star
            if save_data[198] & 0x02:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [9]
                }])
            #Buried Aqua Bomb
            if save_data[78] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [10]
                }])
            #Star C Buried Chest
            if save_data[78] & 0x08:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [11]
                }])
            #Reel Em In
            if save_data[307] & 0x01:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [12]
                }])


            print(len(ctx.items_received))
            if len(ctx.items_received)> 0:
                self.last_received_item = len(ctx.items_received)
                print(ctx.items_received)
                #ITEMS HANDLED HERE
            await self.distribute_pieces(ctx, ctx.items_received, save_data)

            await self.calc_tokens(ctx, ctx.items_received, save_data)
            await self.give_items(ctx, ctx.items_received, save_data)

            #await bizhawk.write(ctx.bizhawk_ctx, address, values[1].to_bytes(values[2]))

            # Send game clear
            if not ctx.finished_game and (save_data[168] & 0x08):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])



        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass