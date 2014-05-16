BEGIN {
    FS = "\t"
  }
  {

    if ($4 =="politics" && $24 >= 1)
    print $12, "\t", $4

  }
