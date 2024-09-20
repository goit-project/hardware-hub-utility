---------------------------------------------------------------------------
--! @file /*file name*/
--! @author TODO
---------------------------------------------------------------------------
library ieee;
use ieee.std_logic_1164.all;

--! @brief TODO
--!
--! @param TODO
entity /*component name*/ is
  generic(
    gen : NATURAL
  );
  port(
    clk : in std_logic;
    arst : in std_logic
  );
end entity;

architecture RTL of /*component name*/ is
begin
  -- reg-state logic
  process(clk, arst)
  begin
    if arst = '1' then
    elsif rising_edge(clk) then
    end if;
  end process;

  -- next-state logic

  -- outputs

end architecture;
