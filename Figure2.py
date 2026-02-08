from __Global__ import *

class plot_time_series():
    def __init__(self):
        self.map_width = 13 * centimeter_factor
        self.map_height = 8.2 * centimeter_factor

    def run(self):
        self.plot_LAIpercentile()

    def plot_LAIpercentile(self):
        df = T.load_df(result_root + rf'\Upload_Data\Figure2\time_series\\Dataframe_area_weighted.df')
        df = self.df_clean(df)
        print(len(df))

        variable_list = ['composite_LAImax_mean',
                         'composite_LAImin_mean',

                         'composite_LAIp95_mean',
                         'composite_LAIp90_mean',
                         'composite_LAIp80_mean',
                         'composite_LAIp70_mean',
                         'composite_LAIp60_mean',

                         'composite_LAIp40_mean',
                         'composite_LAIp30_mean',
                         'composite_LAIp20_mean',
                         'composite_LAIp10_mean',
                         'composite_LAIp5_mean',

                         ]

        # variable_list = ['composite_LAImax_mean',
        #                  'composite_LAImin_mean',
        #
        #                  # 'composite_LAIp99_mean',
        #                  'composite_LAIp95_mean',
        #                  'composite_LAIp90_mean',
        #                  'composite_LAIp80_mean',
        #                  'composite_LAIp20_mean',
        #
        #                  'composite_LAIp10_mean',
        #                  'composite_LAIp5_mean',
        #                  # 'composite_LAIp1_mean',
        #
        #
        #                  ]

        dic_label = {'composite_LAImax_mean': 'LAImax',
                     'composite_LAImin_mean': 'LAImin',
                     'composite_LAIp99_mean': 'LAIp99',
                     'composite_LAIp1_mean': 'LAIp1',
                     'composite_LAIp10_mean': 'LAIp10',
                     'composite_LAIp90_mean': 'LAIp90',
                     'composite_LAIp5_mean': 'LAIp5',
                     'composite_LAIp95_mean': 'LAIp95',
                     'composite_LAIp60_mean': 'LAIp60',
                     'composite_LAIp70_mean': 'LAIp70',
                     'composite_LAIp80_mean': 'LAIp80',
                     'composite_LAIp20_mean': 'LAIp20',
                     'composite_LAIp30_mean': 'LAIp30',
                     'composite_LAIp40_mean': 'LAIp40',

                     }

        color_dic = {

            'composite_LAImax_mean': '#26269A',
            'composite_LAImin_mean': '#D23F4D',
            'composite_LAIp95_mean': '#5D4F9D',
            'composite_LAIp5_mean': '#F36A31',

            'composite_LAIp80_mean': 'teal',
            'composite_LAIp20_mean': 'lightcoral',
            'composite_LAIp60_mean': 'yellowgreen',
            'composite_LAIp70_mean': 'cyan',
            'composite_LAIp30_mean': 'olive',
            'composite_LAIp40_mean': 'gold',

            'composite_LAIp99_mean': 'blue',
            'composite_LAIp1_mean': 'red',
            'composite_LAIp10_mean': '#F8AF66',
            'composite_LAIp90_mean': '#2A85BA',

        }

        year_list = range(0, 25)
        result_dic = {}
        std_dic = {}

        # === 计算每个窗口的均值和标准差 ===
        for var in variable_list:
            mean_dic, std_dic_i = {}, {}
            for year in year_list:
                df_i = df[df['window'] == year]
                ## scheme1
                vals = np.array(df_i[f'{var}'].tolist(), dtype=float)
                weight = np.array(df_i['area_weight'].tolist(), dtype=float)
                weighted_mean_values = (
                        np.nansum(vals * weight)
                        / np.nansum(weight * np.isfinite(vals))
                )

                # print(year, weighted_mean_values)
                ## scheme2
                # vals = np.array(df_i[f'{var}'].tolist(), dtype=float)
                # weighted_mean_values = np.nanmean(vals)

                mean_dic[year] = weighted_mean_values

            result_dic[var] = mean_dic
            std_dic[var] = std_dic_i

        df_mean = pd.DataFrame(result_dic)

        # === 绘图 ===
        plt.figure(figsize=(map_width * 1.8, map_height))
        legendmap = {
            'LAImax': 'LAImax',
            'LAImin': 'LAImin',
            'LAIp99': '99th',
            'LAIp95': '95th',
            'LAIp90': '90th',
            'LAIp10': '10th',
            'LAIp5': '5th',
            'LAIp1': '1st',
            'LAIp80': '80th',
            'LAIp60': '60th',
            'LAIp40': '40th',
            'LAIp20': '20th',
            'LAIp70': '70th',
            'LAIp30': '30th',

        }

        for var in variable_list:
            color = color_dic[var]

            # 计算线和阴影区
            y = df_mean[var]
            # yerr = df_std[var]
            years = list(year_list)

            # 背景阴影 (mean ± std)
            # plt.fill_between(years,
            #                  y - yerr,
            #                  y + yerr,
            #                  color=color,
            #                  alpha=0.1)

            # 主趋势线
            plt.plot(years, y, color=color, linewidth=2,
                     label=legendmap[dic_label[var]], marker='o', markersize=5)

            # 拟合趋势线 + 注释
            slope, intercept, r_value, p_value, std_err = stats.linregress(years, y)
            print(var, slope, p_value)
            x_pos = max(years) * 0.85
            y_pos = y.mean()
            # plt.text(x_pos, y_pos + 1.5, f'{dic_label[var]} slope={slope:.3f}', fontsize=10, color=color)
            # plt.text(x_pos, y_pos - 12, f'p={p_value:.3f}', fontsize=10, color=color)

        # === X轴标签（15年滑窗） ===
        window_size = 15
        year_range = range(1982, 2021)
        year_range_str = []
        for year in year_range:
            start_year = year
            end_year = year + window_size - 1
            if end_year > 2021:
                break
            year_range_str.append(f'{start_year}-{end_year}')

        plt.yticks(fontsize=12)
        plt.xticks(range(len(year_range_str))[::3], year_range_str[::3], rotation=45, ha='right', fontsize=12)

        plt.ylabel('Relative change(%)', fontsize=12)
        # plt.grid(alpha=0.4)
        # plt.legend(fontsize=10, loc='lower right')
        # plt.tight_layout()
        plt.show()

        # out_pdf_fdir = result_root + rf'FIGURE\\weighted_area\\'
        # T.mk_dir(out_pdf_fdir)
        # plt.savefig(out_pdf_fdir + 'time_series_LAIpercentile_SI_nolengend.pdf', dpi=300, bbox_inches='tight')
        # plt.close()

        pass

    def df_clean(self, df):
        T.print_head_n(df)
        # df = df.dropna(subset=[self.y_variable])
        # T.print_head_n(df)
        # exit()
        df = df[df['row'] > 60]
        df = df[df['Aridity'] < 0.65]
        df = df[df['LC_max'] < 10]
        df = df[df['MODIS_LUCC'] != 12]

        df = df[df['landcover_classfication'] != 'Cropland']

        return df


class bivariate():
    def run(self):
        self.bivariate_map()
        pass
    def bivariate_map(self):  ## figure 1  ## LAImin and LAImax bivariate
        import xymap

        fdir = result_root + rf'Upload_Data\Figure2\spatial\\\\'

        outdir = result_root + (rf'Upload_Data\\Figure\\Figure2')

        T.mkdir(outdir)

        # outtif = join(outdir,'CV_trend2.tif')
        outtif = join(outdir, 'LAImax_min_mean.tif')

        fpath1 = join(fdir, 'composite_LAImax_mean_trend.tif')

        fpath2 = join(fdir, 'composite_LAImin_mean_trend.tif')

        # 1
        tif1_label, tif2_label = 'LAImax_trend', 'LAImin_trend'
        # 2
        # tif1_label, tif2_label = 'LAI_CV_trend','LAI_relative_change_mean_trend'

        # 1
        min1, max1 = -1, 1
        min2, max2 = -1, 1

        # 2
        # min1, max1 = -.3, .3
        # min2, max2 = -.5, .5

        arr1 = ToRaster().raster2array(fpath1)[0]
        arr2 = ToRaster().raster2array(fpath2)[0]

        arr1[arr1 < -9999] = np.nan
        arr2[arr2 < -9999] = np.nan

        arr1_flattened = arr1.flatten()
        arr2_flattened = arr2.flatten()

        # plt.hist(arr1_flattened,bins=100)
        # plt.title('arr1')
        # plt.figure()
        # plt.hist(arr2_flattened,bins=100)
        # plt.title('arr2')
        # plt.show()

        # choice 1
        upper_left_color = (0, 0, 110)
        upper_right_color = (112, 196, 181)
        lower_left_color = (237, 125, 49)

        lower_right_color = (193, 92, 156)
        center_color = (240, 240, 240)

        ## CV greening option
        #
        # upper_left_color = (194, 0, 120)
        # upper_right_color = (0,170,237)
        # lower_left_color = (233, 55, 43)
        # # lower_right_color = (160, 108, 168)
        # lower_right_color = (234, 233, 46)
        # center_color = (240, 240, 240)

        xymap.Bivariate_plot_1(res=11,
                               alpha=255,
                               upper_left_color=upper_left_color,  #
                               upper_right_color=upper_right_color,  #
                               lower_left_color=lower_left_color,  #
                               lower_right_color=lower_right_color,  #
                               center_color=center_color).plot_bivariate(
            fpath1, fpath2,
            tif1_label, tif2_label,
            min1, max1,
            min2, max2,
            outtif,
            n_x=5, n_y=5
        )

        T.open_path_and_file(outdir)

    pass


def main():
    # plot_time_series().run()
    bivariate().run()


    pass

if __name__ == '__main__':
    main()