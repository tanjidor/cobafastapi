from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import seaborn as sns

def cleaning_data(data):
    kolom = ['tanggal', 'dosen', 'prodi', 'tahun_akademik', 'kelas', 'matakuliah']
    df = pd.read_csv(data, sep=';', names=kolom, header=None)
    df['dosen'] = df['dosen'].str.upper()
    df['tanggal'] = pd.to_datetime(df['tanggal'])
    df['month'] = df['tanggal'].dt.month
    df['year'] = df['tanggal'].dt.year
    df['week'] = df['tanggal'].dt.isocalendar().week

    df.prodi.replace(51, 'Teknik Sipil', inplace=True)
    df.prodi.replace(53, 'Teknik Informatika', inplace=True)
    df.prodi.replace(52, 'Teknik Industri', inplace=True)

    return df

def fakultas_bar(tod):
    rev_month = tod.groupby(["prodi"])['Percentage'].aggregate(np.mean).reset_index().sort_values('Percentage', ascending=False)
    fig = plt.figure(figsize = (10,6))
    color = sns.color_palette('tab20b', 3)
    ax = sns.barplot(data=rev_month, x='prodi', y='Percentage', palette=color)

    for i in ax.containers:
        ax.bar_label(i, padding=-57, color='white',
                fontsize=10, label_type='edge',
                fontweight='bold',
                fmt='%.2f%%')

    plt.ylabel('Percentage', size=10)
    plt.title('Persentase Kehadiran Fakultas', size=10)
    ax.spines[['right', 'top', 'bottom']].set_visible(False)
    ax.xaxis.set_visible(True)
    plt.savefig("gambar/persentase-kehadiran-fakultas.png",dpi=300, bbox_inches="tight")

def get_tabel_data(df, prodi=None):
    if prodi:
        df = df[df['prodi'] == prodi]
    fak = df.drop(['tanggal', 'month', 'year', 'week'], axis=1)

    tod = fak.value_counts().reset_index()
    tod.rename(columns={'count': 'total'}, inplace=True)
    tod = tod.assign(Percentage = lambda x: (x['total'] /16 * 100))

    new_list = []

    def get_new_list(row):
        ea = df[(df['dosen'] == row['dosen']) & (df['kelas'] == row['kelas']) & (df['matakuliah'] == row['matakuliah'])]
        counted = (ea['month']
                        .value_counts()
                    .reset_index(name='counts')
                    .rename({'index': 'month'}, axis=1)
                    .sort_values('month', ascending=True))
        new_list.append(counted['counts'].to_list())

    jing = tod.tail(10)
    for index, row in jing.iterrows():
        get_new_list(row)

    jing['track_record'] = new_list
    return jing, tod

def draw_tabel(df, lingkup, title, nama_file=None):
  if lingkup == 'fakultas':
    col_dosen = df.dosen.to_list()
    col_dosen.insert(0, 'Dosen')
    col_prodi = df.prodi.to_list()
    col_prodi.insert(0, 'Prodi')
    col_matkul = df.matakuliah.to_list()
    col_matkul.insert(0, 'Mata Kuliah')
    col_kelas = df.kelas.to_list()
    col_kelas.insert(0, 'Kelas')
    col_percentage = df.Percentage.to_list()
    col_percentage.insert(0, 'Persentase')
    col_tr = df.track_record.to_numpy()
    col_tr = np.insert(col_tr,0,'Grafik')

    fig, axes = plt.subplots(ncols=6, nrows=11, figsize=(12,4),
                            gridspec_kw={"width_ratios":[1,0.5,2,1,1,0.6]})
    fig.subplots_adjust(0.05,0.05,0.95,0.95, wspace=0.05, hspace=0)

    for ax in axes.flatten():
        ax.tick_params(labelbottom=0, labelleft=0, bottom=0, top=0, left=0, right=0)
        ax.ticklabel_format(useOffset=False, style="plain")
        for _,s in ax.spines.items():
            s.set_visible(False)
    fig.subplots_adjust(top=0.8)
    fig.tight_layout()
    fig.suptitle(title, y=1.15)
    colors = ['deepskyblue', 'orchid','snow','orchid','snow','orchid','snow',
              'orchid','snow','orchid','snow',]
    for ax,color in zip(axes[:,0],colors):
        bbox = ax.get_position()
        rect = Rectangle((0,bbox.y0),1,bbox.height*1.68, color=color, zorder=-1, transform=fig.transFigure, clip_on=False)
        ax.add_artist(rect)
    for ax in axes.flat:
        ax.patch.set_visible(False)

    text_kw = dict(ha="center", va="bottom", size=8)
    text_dsn = dict(ha="left", va="bottom", size=8)
    text_head = dict(ha="center", va="bottom", size=8, weight='bold')
    for i,ax in enumerate(axes[:,0]):
        if i == 0:
          ax.text(0.5, 0.05, col_dosen[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0, 0.05, col_dosen[i], transform=ax.transAxes, **text_dsn)
    for i,ax in enumerate(axes[:,1]):
        if i == 0:
          ax.text(0.8, 0.05, col_prodi[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.8, 0.05, col_prodi[i],transform=ax.transAxes, **text_kw)
    for i,ax in enumerate(axes[:,2]):
        if i == 0:
          ax.text(0.5, 0.05, col_matkul[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.5, 0.05, col_matkul[i],transform=ax.transAxes, **text_kw)
    for i,ax in enumerate(axes[:,3]):
        if i == 0:
          ax.text(0.5, 0.05, col_kelas[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.5, 0.05, col_kelas[i],transform=ax.transAxes, **text_kw)
    for i,ax in enumerate(axes[:,4]):
        if i == 0:
          ax.text(0.5, 0.05, col_percentage[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.5, 0.05, col_percentage[i],transform=ax.transAxes, **text_kw)

    for i,ax in enumerate(axes[:,5]):
        if i == 0:
          ax.text(0.5, 0.05, col_tr[i],transform=ax.transAxes, **text_head)
        ax.plot(col_tr[i], color="indigo", linewidth=1)

    plt.savefig("gambar/tabel-fakultas.png",dpi=300, bbox_inches="tight")


  elif lingkup == 'prodi':
    col_dosen = df.dosen.to_list()
    col_dosen.insert(0, 'Dosen')
    col_matkul = df.matakuliah.to_list()
    col_matkul.insert(0, 'Mata Kuliah')
    col_kelas = df.kelas.to_list()
    col_kelas.insert(0, 'Kelas')
    col_percentage = df.Percentage.to_list()
    col_percentage.insert(0, 'Persentase')
    col_tr = df.track_record.to_numpy()
    col_tr = np.insert(col_tr,0,'Grafik')

    fig, axes = plt.subplots(ncols=5, nrows=11, figsize=(12,4),
                            gridspec_kw={"width_ratios":[1,2,1,1,0.6]})
    fig.subplots_adjust(0.05,0.05,0.95,0.95, wspace=0.05, hspace=0)

    for ax in axes.flatten():
        ax.tick_params(labelbottom=0, labelleft=0, bottom=0, top=0, left=0, right=0)
        ax.ticklabel_format(useOffset=False, style="plain")
        for _,s in ax.spines.items():
            s.set_visible(False)
    fig.subplots_adjust(top=0.8)
    fig.tight_layout()
    fig.suptitle(title, y=1.15)
    colors = ['deepskyblue', 'orchid','snow','orchid','snow','orchid','snow',
              'orchid','snow','orchid','snow',]
    for ax,color in zip(axes[:,0],colors):
        bbox = ax.get_position()
        rect = Rectangle((0,bbox.y0),1,bbox.height*1.68, color=color, zorder=-1, transform=fig.transFigure, clip_on=False)
        ax.add_artist(rect)
    for ax in axes.flat:
        ax.patch.set_visible(False)

    text_kw = dict(ha="center", va="bottom", size=8)
    text_dsn = dict(ha="left", va="bottom", size=8)
    text_head = dict(ha="center", va="bottom", size=8, weight='bold')
    for i,ax in enumerate(axes[:,0]):
        if i == 0:
          ax.text(0.5, 0.05, col_dosen[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0, 0.05, col_dosen[i], transform=ax.transAxes, **text_dsn)
    for i,ax in enumerate(axes[:,1]):
        if i == 0:
          ax.text(0.5, 0.05, col_matkul[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.5, 0.05, col_matkul[i],transform=ax.transAxes, **text_kw)
    for i,ax in enumerate(axes[:,2]):
        if i == 0:
          ax.text(0.5, 0.05, col_kelas[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.5, 0.05, col_kelas[i],transform=ax.transAxes, **text_kw)
    for i,ax in enumerate(axes[:,3]):
        if i == 0:
          ax.text(0.5, 0.05, col_percentage[i], transform=ax.transAxes, **text_head)
        else:
          ax.text(0.5, 0.05, col_percentage[i],transform=ax.transAxes, **text_kw)

    for i,ax in enumerate(axes[:,4]):
        if i == 0:
          ax.text(0.5, 0.05, col_tr[i],transform=ax.transAxes, **text_head)
        ax.plot(col_tr[i], color="indigo", linewidth=1)

    plt.savefig("gambar/{}.png".format(nama_file),dpi=300, bbox_inches="tight")