Inversion identification for:
  -- radiosonde
  -- UM_RA2M
  -- UM_CASIM-100
  -- ECMWF_IFS

Key points in inversion detection:
    -- Greatest dThetaE/dZ below 3km identified as main inversion
    -- Identify second largest gradient; if at main inversion k-1, then main inversion reassigned to this index (i.e. strong gradient started at height index below)
    -- If the greatest dThetaE/dZ is at k = 0, 1, or 2 (iterative), then we have a stable surface layer
          -- In this case, look for greatest dThetaE below 2km and reassign as main inversion base

Quicklooks:
      v2/:
          -- ThetaE profiles shown as solid lines
          -- Max gradient in ThetaE indicated on each profile with square marker
          -- all data are shown on the UM vertical grid (i.e. radiosonde and ECMWF_IFS data interpolated)
          -- RHS:
                -- dashed horizontal lines indicate:
                    -- radiosondes: main inversion base height identified by Jutta's code,
                                  discussed in Vuellers et al., 2020 (ACPD)
                    -- models: diagnosed boundary layer height
                -- vertical dots (coloured as UM_RA2M: blue; UM_CASIM-100: green; ECMWF_IFS: orange/red; radiosondes: grey/black)
                    -- cloud fraction by volume ingested into (models) / calculated using (radiosondes) Cloudnet
                          -- all colour maps scale from 0 to 1
                          -- UM_RA2M, UM_CASIM-100, and radiosonde Cloudnet Cvs on UM grid
                          -- ECMWF_IFS Cv on IFS grid
                -- NOTE: Cloudnet Cvs are not available for all radiosonde (6 hourly) timesteps
