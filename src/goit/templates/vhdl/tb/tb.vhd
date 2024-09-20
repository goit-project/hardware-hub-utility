library std;
library ieee;
library uvvm_util;
library vunit_lib;
library osvvm;
library /*lib*/;

context uvvm_util.uvvm_util_context;
context vunit_lib.vunit_context;
context vunit_lib.vc_context;

use std.env.all;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
use ieee.fixed_pkg.all;
use osvvm.RandomPkg.all;
use vunit_lib.com_pkg.all;
use vunit_lib.memory_pkg.all;
use vunit_lib.axi_stream_pkg.all;
use vunit_lib.stream_slave_pkg.all;
use vunit_lib.stream_master_pkg.all;


entity tb is
  generic(
    runner_cfg : string;
    gen        : natural := 1
  );
end entity;


architecture RTL of tb is
  -----------------------------------------------------------------------------
  -- DUT interfacing
  -----------------------------------------------------------------------------
  signal clk  : std_logic := '0';
  signal arst : std_logic := '0';

  -----------------------------------------------------------------------------
  -- Clock related
  -----------------------------------------------------------------------------
  constant CLK_PERIOD : time    := 10 ns;
  signal clk_en       : boolean := true;

  -----------------------------------------------------------------------------
  -- Verification components
  -----------------------------------------------------------------------------

begin

  -----------------------------------------------------------------------------
  -- DUT instantation
  -----------------------------------------------------------------------------
  DUT : entity /*lib*/./*entity*/
  generic map(
    gen
  )
  port map(
    clk, arst
  );

  -----------------------------------------------------------------------------
  -- Clock instantation
  -----------------------------------------------------------------------------
  clock_generator(clk, clk_en, CLK_PERIOD, "TB clock");

  ----------------------------------------------------------------------------
  -- Verification component instantiation
  ----------------------------------------------------------------------------

  -----------------------------------------------------------------------------
  -- Test sequencer
  -----------------------------------------------------------------------------
  process
    ---------------------------------------------------------------------------
    -- Variables
    ---------------------------------------------------------------------------

    ---------------------------------------------------------------------------
    -- Procedures
    ---------------------------------------------------------------------------

  begin
    test_runner_setup(runner, runner_cfg);
    gen_pulse(arst, 1*CLK_PERIOD, "Activated reset for 1 period");

    while test_suite loop
      if run("Full coverage") then
        report "test run works";
      end if;
    end loop;

    test_runner_cleanup(runner);
  end process;

end architecture;
