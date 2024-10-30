import { createStore } from "vuex";

export const store = createStore({
  state: {
    sigma_instance: null,
    gephi_json: null,
    term_graph_data: null,
    term_graph_dict: [],
    citation_graph_dict: [],
    term_heatmap_dict: [],
    sigma_graph_node: null,
    sigma_graph_term: null,
    sigma_graph_subset: null,
    enrichment: null,
    active_node_enrichment: null,
    dcoloumns: null,
    current_enrichment_terms: null,
    colorpalette: null,
    test_sample:
      "Gnai3;Klf6;Xpo6;Gmpr;Trim25;Tbrg4;Mx1;Pdgfb;Zfp385a;Gpcr2;Clcn4-2;Myo18a;Heatr6;Ccl3;Nhp2;Poldip2;Ckb;Smg5;Tubb5;Ell2;Ergic1;Brpf1;Ubl3;Il16;Tcirg1;Rtcb;Rac1;Nfix;Blvra;Celf2;Sf3a1;Ppard;Daxx;Ipo4;Ccdc97;Lcp2;Cse1l;Il17ra;Pnkp;Apoe;Hbp1;Klf4;Ap1m1;Ppp5c;Hck;Keap1;Prkcsh;Ier3;Klc4;Man1a;Nfat5;Stat3;Psap;Ptpn6;Coro1c;Arhgef40;Chn2;Arid3b;Ly9;Cd244;Emr1;Ulk2;Grap;Dtx2;Prkacb;Cstb;Wdr1;Man2b1;Txn2;Hmox1;Por;Trim28;Mef2c;Snx6;Reep5;Nr2c2;Tpr;Dhx34;Inpp5k;Fblim1;Tep1;Tmbim1;Ggt5;Neurl1a;Aprt;Pknox1;B4galnt1;Sod2;M6pr;Tgfbr1;Bcl2l1;Zmiz1;Ctsd;Phax;Snrpb2;Ubc;Sertad1;Vav2;Ubp1;Nuak2;Rassf1;Slc3a2;Tmem86a;Ifi35;Rdm1;Psen2;Vac14;Gltp;Rps5;Etv5;Ptprs;Cacybp;Mertk;Dguok;Csf1;Lrrk1;Actn1;Sirt2;Abca1;Gadd45b;Zdhhc12;Cybb;Atf6b;Hivep2;Nat9;Hspa8;Cers2;Anp32e;Tab2;Rxra;Fcgr1;Ncf1;Cacna1d;Fli1;Slmo2;Slc25a5;Mapkapk2;Lamp2;Pacsin2;Plcg1;Sdc4;Plxdc1;Wsb1;Tha1;Pgs1;Myo1c;Pitpna;Mlx;Ppp2r5c;B4galt5;Med13l;Vmp1;Pmp22;Kansl1;C1qbp;Slc13a3;Kdm6b;Trpv2;Sparc;Ikzf1;Ndel1;Atp5g3;Rars;Arrb1;Ccl4;Ywhah;Fis1;Plod1;Ccl9;BC005537;Rab5c;H13;Ddx39b;Arid3a;Ccdc12;Pcmt1;Aig1;Tnfaip3;Reep3;Ccdc59;Ppp1r12a;Lims1;Rhobtb1;Dusp6;Psen1;Sgk1;Epb4.1l2;Tmcc3;Ccdc53;Srgn;Slc29a3;Vsir;Anapc16;ENSMUSG00000020133;Peli1;Dock2;Cnot2;Nav3;Ncln;Txnrd1;Appl2;Hint1;Stk10;Mdh1;Mgat1;Ppp2ca;Ltc4s;Sar1b;Rtn4;Xbp1;Galnt10;Prpsap2;Srebf1;Tspan13;Rock2;Snx13;Lpin1;Trappc12;Rsad2;Id2;Dnmt3a;Rab10;Itgb3;Adap2;Psmd12;Slc9a3r1;Hn1;Cluh;Trim47;Cpd;Abcc3;Per1;Ctc1;Pik3r5;Nfkbia;Sptlc2;Glrx5;Hif1a;Atp6v1d;Zfp36l1;Susd6;Gtpbp4;Zmynd11;Psmc1;Lgmn;Asb2;Gdi2;Numb;Fos;Tnfaip2;Eif5;Gcnt2;Edn1;Susd3;Eci2;Ly86;Sema4d;Gadd45g;Sptlc1;Ctsl;Rasa1;Golm1;Erap1;Lpcat1;Cd180;Gtf2h2;Hexb;Ap3b1;Scamp1;Erbb2ip;Mrps30;Slc4a7;Il6st;Comtd1;Camk2g;Slmap;Gpr65;Prkcd;Extl3;Atp8a2;Spata13;Lcp1;Bnip3l;Slc39a14;Rcbtb2;Itm2b;Fbxl3;Nipbl;Fyb;Dab2;Slc7a8;Oxct1;Slc22a17;Ngdn;Cct5;Tars;Trio;Fam134b;Pabpc1;Atp6v1c1;Rad21;Mtss1;Sla;Asap1;Fam49b;Syngr1;Csnk1e;Parvg;Myh9;Slc38a2;Nckap1l;Litaf;Zfp263;Fam86;Zbtb20;St3gal6;Tbc1d23;Tomm70a;Dnm1l;Lmln;Itgb5;Hcls1;Senp2;Samsn1;App;Adamts1;Ets2;Cd86;Rcan1;Runx1;Gart;Tmem50b;Ifnar2;Synj1;Sod1;Fmnl3;Dip2b;Atf1;Slc11a2;Prr13;Cdkn1a;Nus1;Rfc2;Denr;Ivns1abp;Vwa5a;Il15ra;Chd1;Tnfrsf12a;Hsp90ab1;Gtpbp2;Tfeb;Trem2;Fgd2;Pim1;Abcg1;Lpin2;Cyp4f13;Man2a1;Vapa;Ralbp1;Srsf7;Dusp1;Fkbp5;Map3k8;Mapre2;Myo1f;Brd2;Tmem173;Hspa9;Bin1;Aif1;Tnf;Riok3;Npc1;Diap1;Gabbr1;Tcerg1;Hsd17b4;Mbd2;Sec11c;Spire1;Snx24;Txnl1;Slc12a2;Psat1;Cyb5a;Fth1;Mrpl16;Lpxn;Ccdc86;Slc15a3;Zfand5;Ehd1;Lipa;Slc25a45;Chka;Pitpnm1;Pold4;Adrbk1;Lrp5;Smarca2;Tcf7l2;Hhex;Xpnpep1;Msr1;Anapc11;Stra13;Slc16a3;Pi4k2a;Scd2;Ldb1;Sat1;Banp;Cd63;Shmt2;Ifitm3;Irf7;Tmc6;Rptor;Cct8;Usp16;Shisa5;Pfkfb4;Sdc3;Nrp1;Pdgfa;Stag2;Hk3;Smad7;Sgk3;Cops5;Tram1;Creb1;Nrp2;Casp8;Ercc5;Il1r2;Stk17b;Stat1;Sema4c;Ptpn18;Dst;Pecr;Atic;Ncl;Ptma;Farsb;Gpr35;Lrrfip1;Hdac4;Cln8;Tnfrsf11a;Ccdc93;Actr3;Ubxn4;Rgs1;Rgs2;Nek7;Srgap2;Adipor1;Ppfia4;Tor1aip1;Glul;Rgl1;Tmem63a;Tagln2;Slamf9;Mpc2;Abl2;Eprs;Batf3;Atf6;Pip4k2a;Plxdc2;Nek6;Pfkfb3;Apbb1ip;Eng;Abl1;Tor1b;Crat;Psmd14;Notch1;Nacc2;Dpp7;Rbms1;Il1rn;Ube2e3;Ssrp1;Itga6;Slc12a6;Commd9;Hsd17b12;Gatm;Zfp106;Vps39;Ehd4;Pcna;Gpcpd1;Spred1;Dusp2;Il1b;Il1a;Rrbp1;Snx5;Sec23b;Cst3;Acss1;Fam110a;Kif3b;Tpd52;Zbp1;Gnas;Ptpn1;Nfatc2;1110008F13Rik;Pik3ca;Actl6a;Ncoa3;Pld1;Ufm1;Mbnl1;Nmd3;Ssr3;Ccnl1;Olfml3;Tpm3;Adar;Tlr2;Gar1;Aimp1;Papss1;Fubp1;Gpatch4;Dapp1;Ppp3ca;Cisd2;Wls;Asph;Pnisr;Ndufaf4;Gbp2;Ube2j1;Akirin2;Ugcg;Snx30;B4galt1;Bag1;Rad23b;Dcaf12;Cd72;Ptplad2;Usp24;Pde4b;Jak1;Nfia;Dyrk2;Slc2a1;Macf1;Ppt1;Fuca1;Pnrc2;Mob3c;Capzb;Eif4g3;Ptp4a2;Ak2;Map7d1;Csf3r;Fgr;Trnau1ap;Sf3a3;Padi2;Pgd;Slc2a5;Fam126a;Mad2l2;Dnajc2;Tprgl;Nadk;Gnb1;Lrpap1;Rnf4;Slc35f6;Tbc1d14;Commd8;Tec;Srd5a3;Aff1;Coq2;Hnrnpdl;Cds1;Ccng2;Rilpl1;Naaa;Slc15a4;Scarb2;Atp2a2;P2rx4;Kdm2b;Ncor2;Sppl3;Psmg3;Tes;Lfng;Tmem106b;Wipi2;Aimp2;Arpc1b;Phf14;Pomp;Cux1;Tsc22d4;Pon3;Exoc4;Tmem176b;Zc3hav1;Zyx;Clec5a;Hpgds;Mkrn1;Tbxas1;Pcyox1;Arhgap25;Cnbp;Foxp1;Arl8b;Ptms;Etv6;Dusp16;Atf7ip;Wbp11;Arhgdib;Ptpro;Strap;Ldhb;Camk1;Itpr2;Cd9;Vasp;Cyfip1;Siglece;Tjp1;Furin;Mef2a;Ctsc;Tyrobp;Nfkbib;Zfand6;Anapc15;Ipo5;Mvp;Fchsd2;Slco2b1;Il21r;Il4ra;Arhgap17;Pak1;Cd37;Stx4a;Rgs10;Mrpl17;Fam53b;Ctbp2;ENSMUSG00000030982;Cask;St5;Slc9a9;Msn;Ophn1;Efnb1;Phka2",
    highlighted_edges: new Set(),
    snapshot_pathways: [],
    snapshot_citations: [],
    favourite_graph_dict: new Set(),
    favourite_heatmaps_dict: new Set(),
    snapshot_heatmaps: [],
    node_cluster_index: {},
    node_modul_index: new Set(),
    node_cluster_index_term: {},
    node_modul_index_term: new Set(),
    active_subset: null,
    p_active_subset: null,
    c_active_subset: null,
    hiding_pathways: new Set(),
    citation_graph_data: null,
    context_dict: {},
    selection: null,
    favourite_subsets: new Set(),
  },
  mutations: {
    assign_sigma_instance(state, value) {
      console.log(value);
      state.sigma_instance = value;
    },
    assign(state, value) {
      state.gephi_json = value;
    },
    assign_selection(state, value) {
      state.selection = value;
    },
    assign_subset(state, value) {
      state.favourite_subsets.add(value);
    },
    delete_subset(state, value) {
      state.favourite_subsets.delete(value);
    },
    assign_colorpalette(state, value) {
      state.colorpalette = value;
    },
    assign_active_subset(state, value) {
      state.active_subset = value;
    },
    assign_active_pgraph_subset(state, value) {
      state.p_active_subset = value;
    },
    assign_active_cgraph_subset(state, value) {
      state.c_active_subset = value;
    },
    assign_term_graph(state, value) {
      state.term_graph_data = value;
    },
    assign_citation_graph(state, value) {
      state.citation_graph_data = value;
    },
    assign_graph_node(state, value) {
      state.sigma_graph_node = value;
    },
    assign_graph_subset(state, value) {
      state.sigma_graph_subset = value;
    },
    assign_graph_term(state, value) {
      state.sigma_graph_term = value;
    },
    assign_active_enrichment(state, value) {
      state.enrichment = value;
    },
    assign_active_enrichment_node(state, value) {
      state.active_node_enrichment = value;
    },
    assign_current_enrichment_terms(state, value) {
      state.current_enrichment_terms = value;
    },
    assign_dcoloumn(state, value) {
      state.dcoloumns = value;
    },
    assign_new_term_graph(state, value) {
      state.term_graph_dict.push(value);
    },
    assign_term_dict(state, value) {
      state.term_graph_dict = value;
    },
    assign_citation_dict(state, value) {
      state.citation_graph_dict = value;
    },
    assign_new_citation_graph(state, value) {
      state.citation_graph_dict.push(value);
    },
    assign_new_heatmap_graph(state, value) {
      state.term_heatmap_dict.push(value);
    },
    update_heatmap_dict(state, value) {
      state.term_heatmap_dict = value;
    },
    remove_term_graph(state, value) {
      const index = state.term_graph_dict.indexOf(value);
      state.term_graph_dict.splice(index, 1);
    },
    remove_citation_graph(state, value) {
      const index = state.term_graph_dict.indexOf(value);
      state.citation_graph_dict.splice(index, 1);
    },
    assign_favourite_graph(state, value) {
      state.favourite_graph_dict = value;
    },
    assign_favourite_heatmap(state, value) {
      state.favourite_heatmaps_dict = value;
    },
    assign_highlightedSet(state, value) {
      state.highlighted_edges = value;
    },
    assign_snapshotPathway(state, value) {
      state.snapshot_pathways.push(value);
    },
    assign_snapshotCitation(state, value) {
      state.snapshot_citations.push(value);
    },
    assign_snapshotHeatmap(state, value) {
      state.snapshot_heatmaps.push(value);
    },
    remove_snapshotCitation(state, value) {
      state.snapshot_citations = state.snapshot_citations.filter(
        (dictionary) => dictionary.id != value
      );
    },
    remove_snapshotHeatmap(state, value) {
      state.snapshot_heatmaps = state.snapshot_heatmaps.filter(
        (dictionary) => dictionary.id != value
      );
    },
    assign_moduleIndex(state, value) {
      state.node_modul_index = value;
    },
    assign_moduleCluster(state, value) {
      state.node_cluster_index = value;
    },
    assign_moduleIndex_term(state, value) {
      state.node_modul_index_term = value;
    },
    assign_moduleCluster_term(state, value) {
      state.node_cluster_index_term = value;
    },
    assign_hiding_pathways(state, value) {
      state.hiding_pathways = value;
    },
    assign_context_br(state, value) {
      state.context_dict = value;
    },
  },
});
