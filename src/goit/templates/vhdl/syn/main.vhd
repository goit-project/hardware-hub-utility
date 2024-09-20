library ieee;
library /*lib*/;
use ieee.std_logic_1164.all;

entity main is
  generic(
    gen : NATURAL
  );
  port(
    clk  : in std_logic;
    arst : in std_logic
  );
end entity;

architecture RTL of main is
begin

  COMP : entity work./*entity*/
  generic map(
    gen
  )
  port map(
    clk, arst
  );

end architecture;
